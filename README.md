# 🧠 Agents/Workflows Evaluation Pipeline

An automated pipeline for generating, simulating, and evaluating question-answer interactions for agents/workflows using large language models (LLMs) like GPT-4 and Dify. Using MET museum scripts as input for demo purpose.

## 📌 Features

### 1. 📄 Transcript Preprocessing
- **Script:** `preprocess_transcript.py`
- **Function:** Cleans raw museum transcripts for clarity and structure.
- **Techniques:**
  - Removes speaker tags and navigation instructions
  - Splits content into short, standalone sentences
  - Adds inline explanations for obscure concepts
  - Optimized for retrieval in RAG systems

### 2. 🧠 Semantic Sentence Categorization
- **Script:** `preprocess_item_category.py`
- **Function:** Categorizes sentences from improved transcripts into thematic buckets such as `period`, `geography`, `visual_features`, etc.
- **Powered by:** GPT-4, using structured system prompts

### 3. ✍️ Synthetic QA Pair Generation
- **Script:** `create_qa.py` with `eval_prompts.py`
- **Function:** For each artifact:
  - Generates a short introduction (3–5 sentences)
  - Creates three questions (two based on text, one requiring external knowledge)
  - Answers each question, labeling the source (`text` or `external`)
- **Output Format:** JSON

### 4. 🤖 LLM Simulation via Dify API
- **Script:** `dify_helper.py`
- **Function:** Simulates interactive user queries with Dify's chat interface
- **Data Flow:** Sends metadata-rich input (title, artist, culture, etc.) → Receives structured JSON output

## ✅ LLM-Based Evaluation Pipeline

### 5. 🧪 Evaluation Per Artifact
- **Script:** `run_eval_per_object.py`
- **Class:** `AnswerEvaluation`
- **Logic:**
  - Encapsulates artifact-specific logic in a class
  - Compares GPT-generated answers with Dify responses using GPT-based evaluation
  - Uses a rubric for scoring introduction and follow-up questions
  - Stores both numeric scores and qualitative feedback

### 6. 📊 Batch Evaluation
- **Script:** `run_eval_by_batch.py`
- **Class:** `AnswerEvaluationBatch`
- **Function:**
  - Instantiates multiple `AnswerEvaluation` objects
  - Runs intro and follow-up generation concurrently for multiple artifacts
  - Computes average intro and follow-up scores across the batch
  - Enhances efficiency and enables large-scale evaluation

## 🧰 Tech Stack

- **LLMs:** OpenAI GPT-4, Dify
- **Backend:** Python (class-based OOP design for clarity)
- **Database:** Supabase (artifact metadata retrieval)
- **Storage:** JSON for input/output
- **Eval:** GPT-as-a-judge scoring system

---

## 🚀 Getting Started

### 1. **Install dependencies**
   ```bash
   pip install openai supabase requests
   ```
### 2. Set up your .env
   ```bash
   OPENAI_API_KEY=your_openai_key
   DIFY_API_KEY=your_dify_key
   ```
### 3. Run Transcript Processing
   ```bash
   python preprocess_transcript.py
   ```
### 4. Run QA Generation + Evaluation
   ```bash
    python run_eval_by_batch.py
   ```

## 🧪 Example Output

   ```json
    {
      "artifact_id": "544067",
      "introduction": "This is a bronze vessel...",
      "questions": [
        {
          "question": "What material is the object made of?",
          "answer": "Bronze",
          "answer_source": "text"
        },
        ...
      ]
    }
   ```
