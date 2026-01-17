import os
import sys
import logging
from pathlib import Path
from typing import List

import PyPDF2
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document  
from tqdm import tqdm

PDF_PATH = "data/Annual-Report-2024-25.pdf"
VECTOR_DB_PATH = "vectorstore"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def load_pdf_manual(pdf_path: str) -> List[Document]:
    documents = []
    
    print(f"Loading PDF: {pdf_path}")
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        
        print(f"Total pages: {total_pages}")
        
        for page_num in tqdm(range(total_pages), desc="Reading pages"):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
            if text.strip():
                doc = Document(
                    page_content=text,
                    metadata={"page": page_num, "source": pdf_path}
                )
                documents.append(doc)
    
    return documents


def split_text_manual(documents: List[Document], chunk_size: int, overlap: int) -> List[Document]:
    # split documents into chunks
    chunks = []
    
    print(f"Splitting into chunks (size={chunk_size}, overlap={overlap})...")
    
    for doc in tqdm(documents, desc="Splitting documents"):
        text = doc.page_content
        metadata = doc.metadata
        
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            
            if chunk_text.strip():
                chunk = Document(
                    page_content=chunk_text,
                    metadata=metadata.copy()
                )
                chunks.append(chunk)
            
            start += chunk_size - overlap
    
    return chunks


def main():
    if not os.path.exists(PDF_PATH):
        raise FileNotFoundError(f"PDF not found: {PDF_PATH}")

    print("\n" + "="*60)
    print("PDF Ingestion Pipeline")
    print("="*60)

    # Load PDF
    documents = load_pdf_manual(PDF_PATH)
    print(f"✓ Loaded {len(documents)} pages")

    # Split into chunks
    chunks = split_text_manual(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"✓ Created {len(chunks)} chunks")

    # Load embeddings
    print("Loading embeddings model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("✓ Embeddings loaded")

    # Create vector store
    print("Creating FAISS vector store...")
    vectorstore = FAISS.from_documents(
        tqdm(chunks, desc="Embedding chunks"),
        embeddings
    )
    print("✓ Vector store created")

    # Save
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    vectorstore.save_local(VECTOR_DB_PATH)
    print(f"✓ Saved to: {VECTOR_DB_PATH}")

    print("\n" + "="*60)
    print("Ingestion Complete!")
    print("="*60)


if __name__ == "__main__":
    main()