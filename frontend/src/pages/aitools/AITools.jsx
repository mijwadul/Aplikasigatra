import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActionArea,
  Avatar,
  useTheme
} from '@mui/material';
import LibraryBooksIcon from '@mui/icons-material/LibraryBooks';
import SearchIcon from '@mui/icons-material/Search';
import CreateIcon from '@mui/icons-material/Create';
import AssessmentIcon from '@mui/icons-material/Assessment';

function AITools() {
  const navigate = useNavigate();
  const theme = useTheme();

  const tools = [
    {
      title: 'Retriever Dokumen',
      description: 'Ambil & embed dokumen kurikulum dari situs resmi.',
      icon: <LibraryBooksIcon fontSize="large" />,
      path: '/aitools/retriever'
    },
    {
      title: 'Cari Template Kurikulum',
      description: 'Temukan CP, ATP, dst via Google Search API.',
      icon: <SearchIcon fontSize="large" />,
      path: '/aitools/search'
    },
    {
      title: 'Generator Dokumen',
      description: 'Buat RPP, Modul Ajar, CP, dst secara otomatis.',
      icon: <CreateIcon fontSize="large" />,
      path: '/aitools/generator'
    },
    {
      title: 'Evaluasi Otomatis (Segera)',
      description: 'Input nilai & AI bantu analisis pembelajaran.',
      icon: <AssessmentIcon fontSize="large" />,
      path: '#'
    }
  ];

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        🎓 Gatra Sinau.AI — Alat Cerdas untuk Guru
      </Typography>

      <Typography variant="body1" sx={{ mb: 3 }}>
        Pilih fitur di bawah ini untuk membantumu menyelesaikan tugas administratif dengan lebih mudah:
      </Typography>

      <Grid container spacing={3}>
        {tools.map((tool, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card
              sx={{
                height: '100%',
                borderRadius: 3,
                transition: '0.3s',
                '&:hover': {
                  transform: 'scale(1.02)',
                  boxShadow: 6
                },
                backgroundColor: theme.palette.background.paper
              }}
            >
              <CardActionArea onClick={() => tool.path !== '#' && navigate(tool.path)}>
                <CardContent>
                  <Avatar
                    sx={{
                      bgcolor: theme.palette.primary.main,
                      width: 56,
                      height: 56,
                      mb: 1
                    }}
                  >
                    {tool.icon}
                  </Avatar>
                  <Typography variant="h6" sx={{ mt: 1 }}>
                    {tool.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {tool.description}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default AITools;