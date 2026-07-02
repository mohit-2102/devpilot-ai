"use client";
import React from 'react';
import { useState } from 'react';

export default function Home() {

  const [file, setFile] = useState<File | null>(null)

  async function testBackend() {

    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData()
    formData.append("file", file)
    const response = await fetch("http://localhost:8000/upload/file", {
      method: "POST",
      body: formData
    });

    const data = await response.json();

    console.log(data);

    alert("upload successful");
  }

  return (
    <main className="flex min-h-screen items-center justify-center">

      <input type="file"
        placeholder='choose file'
        onChange={(e) => {
          if (e.target.files) {
            setFile(e.target.files[0]);
          }
        }}
      />
      <button
        onClick={testBackend}
        className="rounded-lg bg-black px-6 py-3 text-white"
      >
        Test Backend
      </button>
    </main>
  );
}