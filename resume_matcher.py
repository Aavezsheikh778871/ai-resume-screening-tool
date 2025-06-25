from sentence_transformers import SentenceTransformer, util
from utils import preprocess_text

model = SentenceTransformer('all-MiniLM-L6-v2')

def match_resumes(job_description, resume_texts, resume_names):
    job_desc_processed = preprocess_text(job_description)
    job_embedding = model.encode(job_desc_processed, convert_to_tensor=True)

    results = []
    for name, resume in zip(resume_names, resume_texts):
        resume_processed = preprocess_text(resume)
        resume_embedding = model.encode(resume_processed, convert_to_tensor=True)

        similarity = util.pytorch_cos_sim(job_embedding, resume_embedding).item()

        # Find matched keywords (optional - keep for UI)
        matched_keywords = []
        for word in set(job_desc_processed.split()):
            if word in resume_processed:
                matched_keywords.append(word)

        results.append((name, similarity, matched_keywords))

    return results

