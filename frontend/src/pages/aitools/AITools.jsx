import React from 'react';
import { Button, Typography, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function AITools() {
  const navigate = useNavigate();

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">AI Tools untuk Guru</h1>
      <p className="text-muted-foreground">Pilih fitur AI yang ingin digunakan:</p>

      <div className="space-y-2">
        <Button variant="outline" className="w-full text-left" onClick={() => navigate('/ai/retriever')}>
          📄 Retriever Dokumen Kurikulum
        </Button>
        {/* Tambahkan tools lain di masa depan di sini */}
      </div>
    </div>
  );
}