import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pdf_reader import extract_text_from_pdf
from resume_matcher import match_resumes
import pandas as pd

class ResumeMatcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume Matcher")
        self.root.geometry("500x400")

        self.resume_folder = "resumes"  # Automatically use 'resumes' folder
        self.job_description_path = None

        tk.Label(root, text="📁 Using Default Resume Folder: 'resumes'", fg="green").pack(pady=10)

        tk.Button(root, text="📝 Load Job Description", command=self.load_job_description).pack(pady=10)
        tk.Button(root, text="⚙️ Match Resumes", command=self.run_matching).pack(pady=10)

        self.result_text = tk.Text(root, height=15, width=60)
        self.result_text.pack(pady=10)

    def load_job_description(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            self.job_description_path = path
            messagebox.showinfo("Success", "Job description loaded!")

    def run_matching(self):
        if not self.job_description_path:
            messagebox.showerror("Error", "Please load a job description first.")
            return

        if not os.path.exists(self.resume_folder):
            messagebox.showerror("Error", f"Resume folder '{self.resume_folder}' does not exist.")
            return

        with open(self.job_description_path, 'r', encoding='utf-8') as f:
            job_description = f.read()

        resume_texts = []
        resume_names = []

        for filename in os.listdir(self.resume_folder):
            if filename.endswith('.pdf'):
                path = os.path.join(self.resume_folder, filename)
                text = extract_text_from_pdf(path)
                resume_texts.append(text)
                resume_names.append(filename)

        results = match_resumes(job_description, resume_texts, resume_names)

        # Save all results
        df = pd.DataFrame(results, columns=["Resume Name", "Match Score", "Matched Keywords"])
        df.to_csv("results.csv", index=False)

        # Save top 3
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        top_3 = sorted_results[:3]
        pd.DataFrame(top_3, columns=["Resume Name", "Match Score", "Matched Keywords"]).to_csv("top_3_shortlisted.csv", index=False)

        # Show results in GUI
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "📊 Matching Results:\n\n")
        for name, score, keywords in results:
            self.result_text.insert(tk.END, f"{name}: {score:.2f} | Keywords: {', '.join(keywords)}\n")

        self.result_text.insert(tk.END, "\n🏆 Top 3 Shortlisted:\n\n")
        for name, score, keywords in top_3:
            self.result_text.insert(tk.END, f"{name}: {score:.2f} | Keywords: {', '.join(keywords)}\n")

        messagebox.showinfo("Done", "Matching complete! Results saved to 'results.csv' and 'top_3_shortlisted.csv'.")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeMatcherApp(root)
    root.mainloop()
