# **AI News Event Clustering & Timeline Builder**

---

##  **Project Overview**

In modern media ecosystems, the same real-world event is reported by **hundreds or even thousands of news articles** across different platforms, countries, and dates. This makes it difficult to clearly understand:

- What the actual event is  
- How the event evolved over time  
- What were the key milestones and turning points  

This project builds an **AI-based system** that automatically:

- Groups large volumes of news articles into **real-world events** using unsupervised learning  
- Constructs a **chronological timeline** for each detected event  
- Generates **human-readable event summaries**  
- Presents insights through an **interactive Streamlit dashboard**

The project focuses on:

- Natural Language Processing (NLP)  
- Large-scale text processing  
- Unsupervised machine learning  
- Event storytelling from unstructured data  

---

##  **Dataset Details**

**Source:** GDELT Global News Dataset (latest 1 month)  
**Initial Size:** ~2 million news articles  

###  Original Fields Used
- `date` – Published date  
- `article_title` – Original article title  
- `article_content` – Full article text  
- `source` – News publisher  
- `url` – Article link  

###  Engineered Fields (Created by Me)
- `project_title` – Cleaned and enriched title representation  
- `project_content` – Combined title + article content  
- `clean_text` – Fully cleaned and lemmatized text  
- `event_cluster` – Cluster ID from MiniBatch KMeans  
- `event_label` – Human-readable event name  
- `event_summary` – Short descriptive summary of the event  
- `is_noise` – Flag for unrelated or noisy articles  
- `year_month` – Temporal grouping feature  

To improve performance and storage efficiency, the processed dataset was converted from **CSV → Parquet**.

---

##  **System Architecture & Pipeline**

### 1️⃣ **Data Ingestion & Initial Cleaning**

**Problem:**  
Raw GDELT data is massive, noisy, and inconsistent.

**Solution:**  
- Downloaded the latest 1-month GDELT data  
- Sampled ~2 million articles  
- Standardized column names  
- Handled missing values  
- Converted dates to proper datetime format  

---

### 2️⃣ **Title & Content Engineering (Key Innovation)**

**Challenge Faced:**  
Article titles were highly repetitive, leading to poor clustering and weak event labels.

**How I Solved It:**  
- Combined article title and content into richer representations  
- Created:
  - `project_title`  
  - `project_content`  

This significantly improved semantic quality during clustering.

---

### 3️⃣ **Text Preprocessing**

Steps performed:

- Lowercasing  
- Removing special characters and numbers  
- Stopword removal  
- Lemmatization  

**Final feature created:** `clean_text`

---

### 4️⃣ **Text Representation (Vectorization Strategy)**

**Approaches Tested:**
- Bag of Words  
- Word2Vec  
- Sentence Embeddings  

**Problem:**  
These approaches failed due to memory limitations on 2M+ rows.

**Final Choice:** **HashingVectorizer**

**Why HashingVectorizer?**
- Memory efficient  
- No vocabulary storage required  
- Scales well to very large datasets  
- Stable and fast for sparse text vectors  

---

### 5️⃣ **Event Clustering (Core AI Task)**

**Algorithm Used:** **MiniBatch KMeans**

**Why MiniBatch KMeans?**
- Optimized for large-scale datasets  
- Faster than standard KMeans  
- Lower memory usage  

**Cluster Optimization:**
- Used the **Elbow Method** to determine the optimal number of clusters  

**Noise Handling:**
- Removed very small clusters  
- Filtered irrelevant keyword patterns  
- Flagged unrelated articles as noise  

---

### 6️⃣ **Event Labeling**

For each cluster, I:
- Extracted top keywords  
- Analyzed dominant sources  
- Reviewed recurring themes  

**Example Event Labels:**
- *World Economic Forum – Davos (2026-01)*  
- *US–Venezuela Relations (2026-01)*  
- *India Current Affairs (2026-01)*  

Stored as: `event_label`

---

### 7️⃣ **Timeline Construction**

For each detected event:
- Articles were sorted chronologically  
- Major developments were identified  
- Event progression was captured as a timeline  

This helped transform raw news articles into **story-like event sequences**.

---

### 8️⃣ **Event Summary Generation**

Each event cluster includes an automatically generated summary such as:

> “This event began in late December 2025, experienced major developments in January 2026, and received extensive international media coverage.”

Stored as: `event_summary`

---

### 9️⃣ **User Interface – Streamlit Dashboard**

The final output is presented through a **Streamlit web application** that provides:

- Event selection via dropdown  
- Timeline visualization for top events  
- Event summaries  
- Clickable article links within each event  

---

##  **Key Challenges & Solutions**

| Challenge | Solution |
|--------|--------|
| Extremely large dataset | MiniBatch KMeans + sampling |
| Memory crashes | Switched to HashingVectorizer |
| Poor clustering quality | Combined title and content |
| Noisy articles | Cluster size & keyword filtering |
| Slow processing | Batch processing + Parquet format |

---

##  **Technologies Used**

- Python  
- Pandas, NumPy  
- Scikit-learn  
- Natural Language Processing (NLP)  
- MiniBatch KMeans  
- HashingVectorizer  
- Streamlit  
- Parquet  

---

##  **Project Outcome**

- Clustered millions of news articles into meaningful real-world events  
- Built event timelines showing how stories evolve over time  
- Created a scalable and explainable NLP pipeline  
- Delivered insights through an interactive dashboard  



