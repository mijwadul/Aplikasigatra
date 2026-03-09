import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography, Grid, Button, Paper, CircularProgress } from '@mui/material';
import { motion } from 'framer-motion';
import axios from 'axios';
import AuthContext from '../context/AuthContext';
import SummaryCard from '../components/dashboard/SummaryCard';
import ActivityItem from '../components/dashboard/ActivityItem';
import DashboardImage from '../assets/dashboard.png';
import DescriptionIcon from '@mui/icons-material/Description';
import SchoolIcon from '@mui/icons-material/School';
import ClassOutlinedIcon from '@mui/icons-material/ClassOutlined';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  in: { opacity: 1, y: 0 },
  out: { opacity: 0, y: -20 },
};
const pageTransition = { type: 'tween', ease: 'easeInOut', duration: 0.5 };

function formatTimeAgo(isoString) {
  if (!isoString) return '';
  const date = new Date(isoString);
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);
  if (diffMins < 60) return `${diffMins} menit lalu`;
  if (diffHours < 24) return `${diffHours} jam lalu`;
  if (diffDays < 7) return `${diffDays} hari lalu`;
  return date.toLocaleDateString('id-ID');
}

function DashboardPage() {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      if (!user) return;
      try {
        const token = localStorage.getItem('authToken');
        const res = await axios.get('http://localhost:5000/api/dashboard/stats', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setStats(res.data);
      } catch (err) {
        console.error('Failed to fetch dashboard stats:', err);
        setStats({ documents_count: 0, classes_count: 0, schools_count: 0, recent_activity: [] });
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, [user]);

  const summaryData = stats
    ? [
        { icon: <DescriptionIcon />, value: String(stats.documents_count), label: 'Dokumen AI' },
        { icon: <ClassOutlinedIcon />, value: String(stats.classes_count), label: 'Kelas' },
        { icon: <SchoolIcon />, value: String(stats.schools_count), label: 'Sekolah' },
      ]
    : [];

  const activityData = (stats?.recent_activity || []).map((item) => ({
    icon: <CheckCircleIcon />,
    color: 'success',
    text: `Dokumen "${item.title}" telah disimpan`,
    time: formatTimeAgo(item.created_at),
  }));

  const showSchoolsButton = user && ['Developer', 'School Admin'].includes(user.role);

  return (
    <motion.div initial="initial" animate="in" exit="out" variants={pageVariants} transition={pageTransition} style={{ position: 'relative' }}>
      <Box sx={{ position: 'relative', p: { xs: 2, sm: 3 }, '&::before': { content: { xs: '""', md: 'none' }, position: 'absolute', top: 0, left: 0, right: 0, bottom: 0, backgroundImage: `url(${DashboardImage})`, backgroundSize: 'cover', backgroundPosition: 'center', opacity: 0.1, zIndex: -1, }, }}>
        <Grid container spacing={4} alignItems="center">
          <Grid xs={12} md={7} lg={8}>
            <Box sx={{ mb: 4 }}>
              <Typography variant="h4">Selamat Datang, {user?.username || 'Pengguna'}!</Typography>
              <Typography variant="body1" color="text.secondary">Ini adalah beranda untuk mengelola aktivitas Anda.</Typography>
            </Box>
            <Box sx={{ mb: 4, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button variant="contained" onClick={() => navigate('/docs')}>
                Dokumen AI
              </Button>
              <Button variant="outlined" onClick={() => navigate('/classes')}>
                Manajemen Kelas
              </Button>
              {showSchoolsButton ? (
                <Button variant="outlined" onClick={() => navigate('/schools')}>
                  Manajemen Sekolah
                </Button>
              ) : (
                <Button variant="outlined" onClick={() => navigate('/ai/tools')}>
                  AI Tools
                </Button>
              )}
            </Box>
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                <CircularProgress />
              </Box>
            ) : (
            <Grid container spacing={3}>
              <Grid xs={12} lg={6}>
                <Typography variant="h6" gutterBottom>Ringkasan</Typography>
                {summaryData.map(item => <SummaryCard key={item.label} {...item} />)}
              </Grid>
              <Grid xs={12} lg={6}>
                <Typography variant="h6" gutterBottom>Aktivitas Terbaru</Typography>
                <Paper sx={{ p: 2 }}>
                  {activityData.length > 0 ? (
                    activityData.map((item, idx) => (
                      <ActivityItem key={`${item.text}-${idx}`} {...item} />
                    ))
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      Belum ada aktivitas. Mulai buat dokumen dengan AI Tools.
                    </Typography>
                  )}
                </Paper>
              </Grid>
            </Grid>
            )}
          </Grid>
          <Grid md={5} lg={4} sx={{ display: { xs: 'none', md: 'flex' } }}>
            <Box component="img" src={DashboardImage} alt="Dashboard Illustration" sx={{ width: '100%', maxWidth: 400, mx: 'auto' }}/>
          </Grid>
        </Grid>
      </Box>
    </motion.div>
  );
}
export default DashboardPage;