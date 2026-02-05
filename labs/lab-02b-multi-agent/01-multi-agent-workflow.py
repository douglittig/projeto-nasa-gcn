# Databricks notebook source
# MAGIC %md
# MAGIC # Lab 2B: Multi-Agent Workflow for NASA GCN Analysis
# MAGIC
# MAGIC Este notebook implementa um **workflow multi-agente** para processar e analisar
# MAGIC GCN Circulars usando agentes especializados com LangChain.
# MAGIC
# MAGIC **Baseado no:** O'Reilly Chapter 2 - Multi-Agent Workflow with LangChain
# MAGIC
# MAGIC **Objetivos:**
# MAGIC 1. Implementar workflow de 4 estagios com agentes especializados
# MAGIC 2. Aplicar prompt-task alignment para cada tipo de tarefa
# MAGIC 3. Criar tools reutilizaveis para processamento de GCN
# MAGIC 4. Demonstrar ReAct pattern (Reasoning + Acting)
# MAGIC
# MAGIC **Exam Topics Covered:**
# MAGIC - Section 1: Design (22%)
# MAGIC   - Multi-stage AI workflows with clear task boundaries
# MAGIC   - Prompt-task alignment for different reasoning types
# MAGIC - Section 3: Application Development (30%)
# MAGIC   - LangChain agents and tool composition
# MAGIC   - Modular, testable AI pipeline design

# COMMAND ----------

# MAGIC %md
# MAGIC ## Setup

# COMMAND ----------

# MAGIC %pip install --upgrade langchain langchain-community langchain-core langgraph --quiet
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Imports e Configuracao

# COMMAND ----------

import re
from typing import Dict, List, Any, Optional
from datetime import datetime

from langchain_community.chat_models import ChatDatabricks
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# Configuracao
CATALOG = "sandbox"
SCHEMA = "nasa_gcn_dev"
LLM_ENDPOINT = "databricks-meta-llama-3-1-70b-instruct"

print(f"Catalog: {CATALOG}")
print(f"Schema: {SCHEMA}")
print(f"LLM Endpoint: {LLM_ENDPOINT}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Inicializar LLM
# MAGIC
# MAGIC Usamos o modelo Databricks Foundation Model que e **gratuito** para usuarios Databricks.
# MAGIC Temperatura 0 para respostas deterministicas e consistentes.

# COMMAND ----------

# Inicializar LLM
llm = ChatDatabricks(
    endpoint=LLM_ENDPOINT,
    temperature=0
)

print(f"LLM initialized: {llm.__class__.__name__}")
print(f"Endpoint: {LLM_ENDPOINT}")
print(f"Temperature: 0 (deterministic)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Carregar Dados de GCN Circulars
# MAGIC
# MAGIC Carregamos alguns GCN Circulars para usar como input do workflow multi-agente.

# COMMAND ----------

# Carregar GCN Circulars da tabela Silver
df_circulars = spark.table(f"{CATALOG}.{SCHEMA}.gcn_circulars")

# Pegar alguns exemplos
sample_circulars = df_circulars.select("event_id", "subject", "body").limit(5).toPandas()

print(f"Loaded {len(sample_circulars)} sample GCN Circulars")
display(sample_circulars[["event_id", "subject"]])

# COMMAND ----------

# Exemplo de circular para processamento
sample_text = sample_circulars.iloc[0]["body"]
sample_event = sample_circulars.iloc[0]["event_id"]

print(f"Sample Event: {sample_event}")
print(f"\nCircular Preview (first 500 chars):")
print(sample_text[:500] + "...")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Definir Tools para os Agentes
# MAGIC
# MAGIC ### Conceito-Chave: Tool Composition
# MAGIC
# MAGIC Tools sao funcoes que agentes podem invocar dinamicamente baseado na tarefa.
# MAGIC A **docstring** e critica - o agente usa para decidir quando chamar a tool.
# MAGIC
# MAGIC **Exam Tip:** Tools devem ter docstrings claras e especificas.

# COMMAND ----------

# DBTITLE 1,Tools para Extraction Agent
@tool
def extract_event_type(text: str) -> str:
    """
    Extract the astronomical event type from GCN circular text.
    Returns one of: GRB, GW, Neutrino, X-ray, Optical, Radio, Unknown.
    Use this tool when you need to identify what type of event the circular is about.
    """
    text_lower = text.lower()

    if "gamma-ray burst" in text_lower or "grb" in text_lower:
        return "GRB"
    elif "gravitational wave" in text_lower or " gw " in text_lower:
        return "GW"
    elif "neutrino" in text_lower or "icecube" in text_lower:
        return "Neutrino"
    elif "x-ray" in text_lower or "swift xrt" in text_lower:
        return "X-ray"
    elif "optical" in text_lower or "magnitude" in text_lower:
        return "Optical"
    elif "radio" in text_lower:
        return "Radio"
    else:
        return "Unknown"


@tool
def extract_coordinates(text: str) -> Dict[str, Any]:
    """
    Extract RA (Right Ascension) and Dec (Declination) coordinates from GCN text.
    Returns a dictionary with 'ra', 'dec', and 'format' keys.
    Use this tool when you need to find the sky position of an astronomical event.
    """
    result = {"ra": None, "dec": None, "format": None, "found": False}

    # Pattern 1: RA=XX.XXX, Dec=XX.XXX
    pattern1 = r'RA[=:\s]+(\d+\.?\d*)[,\s]+Dec[=:\s]+([+-]?\d+\.?\d*)'
    match = re.search(pattern1, text, re.IGNORECASE)
    if match:
        result["ra"] = float(match.group(1))
        result["dec"] = float(match.group(2))
        result["format"] = "decimal_degrees"
        result["found"] = True
        return result

    # Pattern 2: HH:MM:SS.SS +DD:MM:SS.S
    pattern2 = r'(\d{1,2}:\d{2}:\d{2}\.?\d*)\s+([+-]?\d{1,2}:\d{2}:\d{2}\.?\d*)'
    match = re.search(pattern2, text)
    if match:
        result["ra"] = match.group(1)
        result["dec"] = match.group(2)
        result["format"] = "sexagesimal"
        result["found"] = True
        return result

    return result


@tool
def extract_instruments(text: str) -> List[str]:
    """
    Extract mentioned instruments and telescopes from GCN text.
    Returns a list of instrument names found in the text.
    Use this tool to identify which observatories or instruments detected or observed the event.
    """
    instruments = []

    known_instruments = [
        "Fermi GBM", "Fermi LAT", "Swift BAT", "Swift XRT", "Swift UVOT",
        "INTEGRAL", "MAXI", "IceCube", "LIGO", "Virgo", "KAGRA",
        "Chandra", "XMM-Newton", "NuSTAR", "HST", "JWST",
        "VLT", "Gemini", "Keck", "Subaru", "NOT", "TNG",
        "ZTF", "ATLAS", "Pan-STARRS", "DECam", "GOTO", "MASTER"
    ]

    text_lower = text.lower()
    for instrument in known_instruments:
        if instrument.lower() in text_lower:
            instruments.append(instrument)

    return list(set(instruments)) if instruments else ["Unknown"]

# COMMAND ----------

# DBTITLE 1,Tools para Validation Agent
@tool
def validate_coordinates(ra: float, dec: float) -> Dict[str, Any]:
    """
    Validate if RA and Dec coordinates are within valid astronomical ranges.
    RA should be 0-360 degrees, Dec should be -90 to +90 degrees.
    Use this tool to verify extracted coordinates are valid.
    """
    result = {"valid": True, "errors": []}

    if ra is not None:
        if not (0 <= ra <= 360):
            result["valid"] = False
            result["errors"].append(f"RA {ra} out of range [0, 360]")
    else:
        result["valid"] = False
        result["errors"].append("RA is missing")

    if dec is not None:
        if not (-90 <= dec <= 90):
            result["valid"] = False
            result["errors"].append(f"Dec {dec} out of range [-90, +90]")
    else:
        result["valid"] = False
        result["errors"].append("Dec is missing")

    return result


@tool
def validate_event_completeness(event_type: str, coordinates: Dict, instruments: List[str]) -> Dict[str, Any]:
    """
    Check if extracted event data is complete enough for analysis.
    Returns validation status and list of missing required fields.
    Use this tool to ensure we have minimum required information about an event.
    """
    result = {"complete": True, "missing": [], "quality_score": 0}

    # Check event type
    if event_type == "Unknown":
        result["complete"] = False
        result["missing"].append("event_type")
    else:
        result["quality_score"] += 30

    # Check coordinates
    if not coordinates.get("found", False):
        result["complete"] = False
        result["missing"].append("coordinates")
    else:
        result["quality_score"] += 40

    # Check instruments
    if instruments == ["Unknown"] or not instruments:
        result["missing"].append("instruments (optional)")
    else:
        result["quality_score"] += 30

    return result

# COMMAND ----------

# DBTITLE 1,Tools para Enrichment Agent
@tool
def classify_event_significance(event_type: str, text: str) -> Dict[str, Any]:
    """
    Classify the scientific significance of the event based on keywords.
    Returns significance level (HIGH, MEDIUM, LOW) and reasons.
    Use this tool to assess how important or interesting the event is.
    """
    text_lower = text.lower()
    significance = {"level": "MEDIUM", "reasons": []}

    # High significance indicators
    high_indicators = [
        "bright", "nearby", "host galaxy", "redshift", "supernova",
        "kilonova", "counterpart", "multi-messenger", "exceptional"
    ]

    # Low significance indicators
    low_indicators = [
        "no detection", "upper limit", "non-detection", "faded below",
        "not visible", "clouded out"
    ]

    high_count = sum(1 for ind in high_indicators if ind in text_lower)
    low_count = sum(1 for ind in low_indicators if ind in text_lower)

    if high_count >= 2:
        significance["level"] = "HIGH"
        significance["reasons"] = [ind for ind in high_indicators if ind in text_lower]
    elif low_count >= 2:
        significance["level"] = "LOW"
        significance["reasons"] = [ind for ind in low_indicators if ind in text_lower]
    else:
        significance["level"] = "MEDIUM"
        significance["reasons"] = ["standard observation report"]

    return significance


@tool
def lookup_event_context(event_type: str) -> Dict[str, str]:
    """
    Provide scientific context about the event type.
    Returns background information useful for understanding the event.
    Use this tool to add educational context about what the event type means.
    """
    context_db = {
        "GRB": {
            "description": "Gamma-Ray Burst - most energetic explosions in the universe",
            "typical_duration": "milliseconds to hours",
            "origin": "collapse of massive stars or neutron star mergers",
            "follow_up_priority": "HIGH - time-critical for afterglow detection"
        },
        "GW": {
            "description": "Gravitational Wave - ripples in spacetime from massive object collisions",
            "typical_duration": "seconds",
            "origin": "black hole or neutron star mergers",
            "follow_up_priority": "CRITICAL - electromagnetic counterpart search"
        },
        "Neutrino": {
            "description": "High-energy neutrino detection from cosmic sources",
            "typical_duration": "instantaneous",
            "origin": "blazars, supernovae, or unknown sources",
            "follow_up_priority": "HIGH - source identification important"
        },
        "X-ray": {
            "description": "X-ray emission from high-energy astrophysical processes",
            "typical_duration": "variable",
            "origin": "various - black holes, neutron stars, supernovae",
            "follow_up_priority": "MEDIUM - depends on source"
        }
    }

    return context_db.get(event_type, {
        "description": "Astronomical transient event",
        "typical_duration": "varies",
        "origin": "unknown",
        "follow_up_priority": "STANDARD"
    })

# COMMAND ----------

# DBTITLE 1,Tools para Summary Agent
@tool
def format_analysis_summary(
    event_id: str,
    event_type: str,
    coordinates: Dict,
    instruments: List[str],
    significance: Dict,
    validation: Dict
) -> str:
    """
    Format all extracted and enriched data into a structured summary.
    Returns a formatted string ready for storage or display.
    Use this tool as the final step to create the output summary.
    """
    summary = f"""
================================================================================
GCN CIRCULAR ANALYSIS SUMMARY
================================================================================

Event ID: {event_id}
Event Type: {event_type}
Analysis Timestamp: {datetime.now().isoformat()}

COORDINATES:
  Found: {coordinates.get('found', False)}
  RA: {coordinates.get('ra', 'N/A')}
  Dec: {coordinates.get('dec', 'N/A')}
  Format: {coordinates.get('format', 'N/A')}

INSTRUMENTS DETECTED:
  {', '.join(instruments) if instruments else 'None identified'}

VALIDATION:
  Data Complete: {validation.get('complete', False)}
  Quality Score: {validation.get('quality_score', 0)}/100
  Missing Fields: {', '.join(validation.get('missing', [])) or 'None'}

SIGNIFICANCE ASSESSMENT:
  Level: {significance.get('level', 'UNKNOWN')}
  Reasons: {', '.join(significance.get('reasons', [])) or 'N/A'}

================================================================================
"""
    return summary


@tool
def extract_key_highlights(text: str) -> List[str]:
    """
    Extract key scientific highlights from the GCN text.
    Returns a list of the most important findings or observations.
    Use this tool to identify the main takeaways from the circular.
    """
    highlights = []

    # Look for key patterns
    patterns = [
        (r'T90[=:\s]+(\d+\.?\d*\s*s)', "T90 duration"),
        (r'redshift[=:\s]+z[=:\s]*(\d+\.?\d*)', "Redshift measured"),
        (r'peak flux[=:\s]+(\d+\.?\d*)', "Peak flux measured"),
        (r'magnitude[=:\s]+(\d+\.?\d*)', "Magnitude measured"),
        (r'(detected|observed) (by|with) ([A-Za-z\s]+)', "Detection"),
    ]

    for pattern, label in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            highlights.append(f"{label}: {match.group(0)}")

    if not highlights:
        highlights.append("Standard observation report - no exceptional findings")

    return highlights[:5]  # Limit to top 5

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Criar Prompts Especializados
# MAGIC
# MAGIC ### Conceito-Chave: Prompt-Task Alignment
# MAGIC
# MAGIC Cada agente precisa de um prompt **especializado** para sua tarefa:
# MAGIC
# MAGIC | Agent | Task Type | Prompt Focus |
# MAGIC |-------|-----------|--------------|
# MAGIC | Extraction | Information Extraction | Structured output, field identification |
# MAGIC | Validation | Classification | Pass/Fail criteria, error detection |
# MAGIC | Enrichment | Reasoning | Domain knowledge application |
# MAGIC | Summary | Generation | Formatting, key highlights |

# COMMAND ----------

# Prompts especializados para cada agente

extraction_system_prompt = """You are a specialized GCN Circular data extraction agent.

Your task is to extract structured information from astronomical circular text.
You have access to tools for extracting:
- Event type (GRB, GW, Neutrino, etc.)
- Coordinates (RA, Dec)
- Instruments that detected the event

RULES:
1. Use the appropriate tool for each piece of information
2. Extract ALL available information from the text
3. Be precise - use exact values when found
4. Report "Unknown" or "Not found" if information is missing
5. Do not infer or assume information not explicitly stated

Process the circular systematically and extract all relevant fields."""


validation_system_prompt = """You are a data validation agent for astronomical observations.

Your task is to validate extracted data from GCN Circulars.
You have access to validation tools to check:
- Coordinate validity (RA 0-360, Dec -90 to +90)
- Data completeness (required vs optional fields)

RULES:
1. Validate ALL extracted data before it's used downstream
2. Flag any invalid or suspicious values
3. Calculate quality scores based on completeness
4. Be strict - invalid data causes problems in analysis
5. Provide clear error messages for any failures"""


enrichment_system_prompt = """You are a scientific enrichment agent for astronomical events.

Your task is to add scientific context and classification to GCN events.
You have access to tools for:
- Classifying event significance (HIGH/MEDIUM/LOW)
- Looking up scientific context about event types

RULES:
1. Assess significance based on keywords and context
2. Add relevant background information
3. Consider multi-messenger implications
4. Be objective in your assessment
5. Focus on actionable scientific insights"""


summary_system_prompt = """You are a summary generation agent for GCN analysis.

Your task is to create a comprehensive, structured summary of the analysis.
You have access to tools for:
- Formatting the final summary
- Extracting key highlights

RULES:
1. Create clear, well-organized output
2. Include ALL analyzed information
3. Highlight the most important findings
4. Make the summary actionable for astronomers
5. Use consistent formatting"""

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. Implementar Workflow Multi-Agente
# MAGIC
# MAGIC ### Conceito-Chave: ReAct Pattern
# MAGIC
# MAGIC O padrao **ReAct** (Reasoning + Acting):
# MAGIC 1. **Reason**: Agente analisa a situacao
# MAGIC 2. **Act**: Agente invoca uma tool
# MAGIC 3. **Observe**: Agente processa o resultado
# MAGIC 4. **Repeat**: Ate completar a tarefa
# MAGIC
# MAGIC **Exam Tip:** Entenda como agentes decidem qual tool chamar baseado no contexto.

# COMMAND ----------

# DBTITLE 1,Classe para Workflow Multi-Agente
class GCNMultiAgentWorkflow:
    """
    Multi-agent workflow for processing GCN Circulars.

    Implements a 4-stage pipeline:
    1. Extraction - Extract structured data from text
    2. Validation - Validate extracted data
    3. Enrichment - Add scientific context
    4. Summary - Generate final report
    """

    def __init__(self, llm):
        self.llm = llm
        self.results = {}

    def run_extraction(self, circular_text: str) -> Dict[str, Any]:
        """Stage 1: Extract structured information from circular."""
        print("\n" + "="*60)
        print("STAGE 1: EXTRACTION")
        print("="*60)

        # Call extraction tools directly (simulating agent behavior)
        event_type = extract_event_type.invoke(circular_text)
        coordinates = extract_coordinates.invoke(circular_text)
        instruments = extract_instruments.invoke(circular_text)

        result = {
            "event_type": event_type,
            "coordinates": coordinates,
            "instruments": instruments
        }

        print(f"Event Type: {event_type}")
        print(f"Coordinates Found: {coordinates.get('found')}")
        print(f"Instruments: {instruments}")

        self.results["extraction"] = result
        return result

    def run_validation(self, extraction_result: Dict) -> Dict[str, Any]:
        """Stage 2: Validate extracted data."""
        print("\n" + "="*60)
        print("STAGE 2: VALIDATION")
        print("="*60)

        coords = extraction_result["coordinates"]
        coord_validation = {"valid": True, "errors": []}

        if coords.get("found") and coords.get("format") == "decimal_degrees":
            coord_validation = validate_coordinates.invoke({
                "ra": coords["ra"],
                "dec": coords["dec"]
            })

        completeness = validate_event_completeness.invoke({
            "event_type": extraction_result["event_type"],
            "coordinates": extraction_result["coordinates"],
            "instruments": extraction_result["instruments"]
        })

        result = {
            "coordinate_validation": coord_validation,
            "completeness": completeness
        }

        print(f"Coordinates Valid: {coord_validation.get('valid')}")
        print(f"Data Complete: {completeness.get('complete')}")
        print(f"Quality Score: {completeness.get('quality_score')}/100")

        self.results["validation"] = result
        return result

    def run_enrichment(self, extraction_result: Dict, circular_text: str) -> Dict[str, Any]:
        """Stage 3: Enrich with scientific context."""
        print("\n" + "="*60)
        print("STAGE 3: ENRICHMENT")
        print("="*60)

        significance = classify_event_significance.invoke({
            "event_type": extraction_result["event_type"],
            "text": circular_text
        })

        context = lookup_event_context.invoke(extraction_result["event_type"])

        highlights = extract_key_highlights.invoke(circular_text)

        result = {
            "significance": significance,
            "context": context,
            "highlights": highlights
        }

        print(f"Significance: {significance.get('level')}")
        print(f"Context: {context.get('description', 'N/A')[:50]}...")
        print(f"Highlights: {len(highlights)} found")

        self.results["enrichment"] = result
        return result

    def run_summary(self, event_id: str) -> str:
        """Stage 4: Generate final summary."""
        print("\n" + "="*60)
        print("STAGE 4: SUMMARY")
        print("="*60)

        summary = format_analysis_summary.invoke({
            "event_id": event_id,
            "event_type": self.results["extraction"]["event_type"],
            "coordinates": self.results["extraction"]["coordinates"],
            "instruments": self.results["extraction"]["instruments"],
            "significance": self.results["enrichment"]["significance"],
            "validation": self.results["validation"]["completeness"]
        })

        self.results["summary"] = summary
        return summary

    def process_circular(self, event_id: str, circular_text: str) -> Dict[str, Any]:
        """Run the complete 4-stage workflow."""
        print("\n" + "="*80)
        print(f"PROCESSING GCN CIRCULAR: {event_id}")
        print("="*80)

        # Stage 1: Extraction
        extraction = self.run_extraction(circular_text)

        # Stage 2: Validation
        validation = self.run_validation(extraction)

        # Stage 3: Enrichment
        enrichment = self.run_enrichment(extraction, circular_text)

        # Stage 4: Summary
        summary = self.run_summary(event_id)

        print("\n" + summary)

        return {
            "event_id": event_id,
            "extraction": extraction,
            "validation": validation,
            "enrichment": enrichment,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. Executar Workflow
# MAGIC
# MAGIC Agora vamos processar um GCN Circular atraves do pipeline multi-agente.

# COMMAND ----------

# Inicializar workflow
workflow = GCNMultiAgentWorkflow(llm)

# Processar circular de exemplo
result = workflow.process_circular(sample_event, sample_text)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 8. Processar Multiplos Circulars
# MAGIC
# MAGIC Demonstrando processamento em batch.

# COMMAND ----------

# Processar todos os circulars de exemplo
all_results = []

for idx, row in sample_circulars.iterrows():
    try:
        result = workflow.process_circular(row["event_id"], row["body"])
        all_results.append(result)
    except Exception as e:
        print(f"Error processing {row['event_id']}: {e}")

print(f"\n\nProcessed {len(all_results)} circulars successfully")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 9. Salvar Resultados
# MAGIC
# MAGIC Salvamos os resultados da analise em uma tabela Delta.

# COMMAND ----------

# Preparar dados para salvar
save_data = []
for r in all_results:
    save_data.append({
        "event_id": r["event_id"],
        "event_type": r["extraction"]["event_type"],
        "coordinates_found": r["extraction"]["coordinates"].get("found", False),
        "ra": r["extraction"]["coordinates"].get("ra"),
        "dec": r["extraction"]["coordinates"].get("dec"),
        "instruments": ",".join(r["extraction"]["instruments"]),
        "quality_score": r["validation"]["completeness"].get("quality_score", 0),
        "significance": r["enrichment"]["significance"].get("level", "UNKNOWN"),
        "highlights": str(r["enrichment"]["highlights"]),
        "processed_at": r["timestamp"]
    })

# Criar DataFrame e salvar
df_results = spark.createDataFrame(save_data)
df_results.write.mode("overwrite").saveAsTable(f"{CATALOG}.{SCHEMA}.gcn_agent_analysis")

print(f"Results saved to {CATALOG}.{SCHEMA}.gcn_agent_analysis")
display(df_results)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 10. Conceitos-Chave para o Exame
# MAGIC
# MAGIC ### Resumo do Workflow Multi-Agente
# MAGIC
# MAGIC | Estagio | Responsabilidade | Tools | Output |
# MAGIC |---------|------------------|-------|--------|
# MAGIC | **Extraction** | Extrair dados estruturados | extract_event_type, extract_coordinates, extract_instruments | Dict com campos extraidos |
# MAGIC | **Validation** | Validar dados | validate_coordinates, validate_completeness | Dict com status de validacao |
# MAGIC | **Enrichment** | Adicionar contexto | classify_significance, lookup_context | Dict com enriquecimento |
# MAGIC | **Summary** | Gerar relatorio | format_summary, extract_highlights | String formatada |
# MAGIC
# MAGIC ### Principios de Design
# MAGIC
# MAGIC 1. **Separation of Concerns**: Cada agente tem uma responsabilidade clara
# MAGIC 2. **Composability**: Tools podem ser reutilizadas
# MAGIC 3. **Testability**: Cada componente testavel isoladamente
# MAGIC 4. **Observability**: Logging em cada estagio
# MAGIC 5. **Scalability**: Design stateless para paralelizacao
# MAGIC
# MAGIC ### Exam Tips
# MAGIC
# MAGIC - Entenda quando usar multi-agent vs single agent
# MAGIC - Saiba como tools sao selecionadas (via docstring)
# MAGIC - Conhca o padrao ReAct (Reason → Act → Observe)
# MAGIC - Prompt-task alignment e critico para cada estagio

# COMMAND ----------

# MAGIC %md
# MAGIC ## 11. Lab Wrap-Up
# MAGIC
# MAGIC ### O que voce aprendeu:
# MAGIC
# MAGIC 1. **Multi-stage workflows** - Pipeline com agentes especializados
# MAGIC 2. **Tool composition** - Criar e registrar tools com @tool decorator
# MAGIC 3. **Prompt-task alignment** - Prompts especificos para cada tipo de tarefa
# MAGIC 4. **ReAct pattern** - Como agentes raciocinam e agem
# MAGIC 5. **Observability** - Logging detalhado para debugging
# MAGIC
# MAGIC ### Proximos Passos:
# MAGIC
# MAGIC 1. **Lab 3: Chunking & Indexing** - Preparar dados para RAG
# MAGIC 2. **Lab 4: RAG App** - Construir aplicacao de Q&A
# MAGIC 3. **Lab 5: Deployment** - Deploy do modelo como endpoint
