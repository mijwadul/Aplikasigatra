import React, { useState } from 'react';
import {
  Box, Typography, TextField, Select, MenuItem,
  FormControl, InputLabel, Button, CircularProgress, Paper
} from '@mui/material';
import axios from 'axios';

function Generator() {
  const [kelas, setKelas] = useState('');
  const [mapel, setMapel] = useState('');
  const [jenis, setJenis] = useState('CP');
  const [loading, setLoading] = useState(false);
  const [hasil, setHasil] = useState('');

  const handleGenerate = async () => {
    setLoading(true);
    setHasil('');
    try {
      const res = await axios.post('http://localhost:5000/api/generate-doc', {
        kelas, mapel, jenis
      });
      setHasil(res.data.text);
    } catch (err) {
      console.error(err);
      alert('Gagal menghasilkan dokumen');
    }
    setLoading(false);
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        🧾 Generator Dokumen Kurikulum
      </Typography>

      <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mb: 3 }}>
        <FormControl size="small" sx={{ minWidth: 120 }}>
          <InputLabel>Jenis</InputLabel>
          <Select value={jenis} label="Jenis" onChange={(e) => setJenis(e.target.value)}>
            <MenuItem value="CP">CP</MenuItem>
            <MenuItem value="ATP">ATP</MenuItem>
            <MenuItem value="Prota">Prota</MenuItem>
            <MenuItem value="Promes">Promes</MenuItem>
            <MenuItem value="Modul Ajar">Modul Ajar</MenuItem>
          </Select>
        </FormControl>

        <TextField size="small" label="Mapel" value={mapel} onChange={(e) => setMapel(e.target.value)} />
        <TextField size="small" label="Kelas" value={kelas} onChange={(e) => setKelas(e.target.value)} />

        <Button onClick={handleGenerate} variant="contained" color="success">
          {loading ? <CircularProgress size={20} /> : 'Generate'}
        </Button>
      </Box>

      {hasil && (
        <Paper elevation={3} sx={{ p: 2, whiteSpace: 'pre-wrap', bgcolor: '#f9f9f9' }}>
          {hasil}
        </Paper>
      )}
    </Box>
  );
}

export default Generator;