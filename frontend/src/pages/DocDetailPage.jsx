import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Box, Typography, Paper, Button, CircularProgress, Divider, Chip, IconButton, Menu, MenuItem, Dialog, DialogTitle, DialogContent, DialogActions, TextField } from '@mui/material';
import { motion } from 'framer-motion';
import AuthContext from '../context/AuthContext';
import CustomAlert from '../components/common/CustomAlert';
import DownloadIcon from '@mui/icons-material/Download';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import MoreVertIcon from '@mui/icons-material/MoreVert';

const pageVariants = {
  initial: { opacity: 0, x: 100 },
  in: { opacity: 1, x: 0 },
  out: { opacity: 0, x: -100 },
};

function DocDetailPage() {
  const { docId } = useParams();
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isDownloading, setIsDownloading] = useState(false);
  const [alertInfo, setAlertInfo] = useState({ show: false, type: 'info', message: '' });
  const [anchorEl, setAnchorEl] = useState(null);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [editContent, setEditContent] = useState('');

  const handleMenuClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleEdit = () => {
    setEditTitle(document.title);
    setEditContent(document.content);
    setEditDialogOpen(true);
    handleMenuClose();
  };

  const handleUpdateDoc = async () => {
    try {
      const token = localStorage.getItem('authToken');
      const res = await axios.put(`http://localhost:5000/api/docs/${docId}`, 
        { 
          title: editTitle,
          content: editContent
        },
        { headers: { Authorization: `Bearer ${token}` }}
      );
      
      console.log('Update response:', res.status, res.data);
      
      // Handle response dengan validasi yang lebih aman
      if (res.status === 200 && res.data) {
        const updatedDoc = res.data.document || res.data;
        if (updatedDoc && updatedDoc.id) {
          setDocument(updatedDoc);
          setEditDialogOpen(false);
          setAlertInfo({ show: true, type: 'success', message: 'Document updated successfully!' });
        } else {
          // Fallback: update dengan data yang ada
          setDocument(prev => ({
            ...prev,
            title: editTitle,
            content: editContent
          }));
          setEditDialogOpen(false);
          setAlertInfo({ show: true, type: 'success', message: 'Document updated successfully!' });
        }
      } else {
        setAlertInfo({ show: true, type: 'error', message: 'Failed to update document: Invalid response' });
      }
    } catch (err) {
      console.error('Update error:', err);
      setAlertInfo({ show: true, type: 'error', message: `Failed to update document: ${err.response?.data?.error || err.message || 'Network error'}` });
    }
  };

  const handleDelete = () => {
    setDeleteDialogOpen(true);
    handleMenuClose();
  };

  const confirmDelete = async () => {
    // Convert docId to number and validate
    const docIdNum = parseInt(docId);
    
    if (!docId || isNaN(docIdNum)) {
      setAlertInfo({ show: true, type: 'error', message: 'Invalid document ID for deletion' });
      return;
    }

    console.log('Attempting to delete document with ID:', docIdNum);
    
    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.delete(`http://localhost:5000/api/docs/${docIdNum}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      console.log('Delete response:', response.status, response.data);
      
      if (response.status === 200) {
        setAlertInfo({ show: true, type: 'success', message: 'Document deleted successfully!' });
        setTimeout(() => navigate('/docs'), 2000);
      } else {
        setAlertInfo({ show: true, type: 'error', message: `Failed to delete document: ${response.data?.error || 'Unknown error'}` });
      }
    } catch (err) {
      console.error('Delete error:', err);
      setAlertInfo({ show: true, type: 'error', message: `Failed to delete document: ${err.response?.data?.error || err.message || 'Network error'}` });
    }
  };

  useEffect(() => {
    const fetchDoc = async () => {
      if (!user || !docId) return;
      try {
        const token = localStorage.getItem('authToken');
        const res = await axios.get(`http://localhost:5000/api/docs/${docId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setDocument(res.data);
      } catch (err) {
        setAlertInfo({ show: true, type: 'error', message: 'Failed to load document.' });
      } finally {
        setLoading(false);
      }
    };
    fetchDoc();
  }, [user, docId]);
  
  const handleDownload = async () => {
    if (!document) return;
    setIsDownloading(true);
    setAlertInfo({ show: false });

    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.post('http://localhost:5000/api/docs/download-pdf', 
        { content: document.content, title: document.title },
        { 
          headers: { Authorization: `Bearer ${token}` },
          responseType: 'blob'
        }
      );

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      const safeFilename = document.title.replace(/[^a-z0-9 ]/gi, '').replace(/ /g, '_') + '.pdf';
      link.setAttribute('download', safeFilename);
      document.body.appendChild(link);
      link.click();

      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);

    } catch (error) {
      console.error("Failed to download PDF:", error);
      setAlertInfo({ show: true, type: 'error', message: 'Failed to create PDF file.' });
    } finally {
      setIsDownloading(false);
    }
  };

  if (loading) {
    return <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}><CircularProgress /></Box>;
  }

  return (
    <motion.div initial="initial" animate="in" exit="out" variants={pageVariants}>
      <Box sx={{ p: { xs: 2, sm: 3 } }}>
        <CustomAlert {...alertInfo} onClose={() => setAlertInfo({ ...alertInfo, show: false })} />
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/docs')} sx={{ mb: 2 }}>
          Back to Documents
        </Button>
        {document ? (
          <Paper elevation={3} sx={{ p: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2, flexWrap: 'wrap', gap: 2 }}>
              <Box>
                <Typography variant="h4">{document.title}</Typography>
                <Chip label={document.document_type} size="small" sx={{ mr: 1, mt: 1 }} />
                <Chip label={document.subject} size="small" sx={{ mt: 1 }} />
              </Box>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Button
                  variant="contained"
                  startIcon={isDownloading ? <CircularProgress size={20} color="inherit" /> : <DownloadIcon />}
                  onClick={handleDownload}
                  disabled={isDownloading}
                >
                  Download PDF
                </Button>
                <IconButton onClick={handleMenuClick}>
                  <MoreVertIcon />
                </IconButton>
              </Box>
            </Box>
            <Divider sx={{ my: 2 }} />
            <Box 
              sx={{ 
                whiteSpace: 'pre-wrap', 
                maxHeight: '70vh', 
                overflowY: 'auto', 
                p: 2, 
                fontFamily: 'default',
                lineHeight: 1.7
              }}
            >
               <Typography 
                 component="div" 
                 dangerouslySetInnerHTML={{ 
                   __html: document.content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br />') 
                 }} 
               />
            </Box>
          </Paper>
        ) : (
          <Typography>Document not found.</Typography>
        )}
        
        {/* Menu untuk Edit dan Delete */}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
        >
          <MenuItem onClick={handleEdit}>
            <EditIcon sx={{ mr: 1 }} />
            Edit
          </MenuItem>
          <MenuItem onClick={handleDelete}>
            <DeleteIcon sx={{ mr: 1 }} />
            Delete
          </MenuItem>
        </Menu>

        {/* Edit Dialog */}
        <Dialog open={editDialogOpen} onClose={() => setEditDialogOpen(false)} maxWidth="md" fullWidth>
          <DialogTitle>Edit Document</DialogTitle>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="Document Title"
              type="text"
              fullWidth
              variant="outlined"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              sx={{ mb: 2 }}
            />
            <TextField
              margin="dense"
              label="Document Content"
              multiline
              rows={12}
              fullWidth
              variant="outlined"
              value={editContent}
              onChange={(e) => setEditContent(e.target.value)}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setEditDialogOpen(false)}>Cancel</Button>
            <Button onClick={handleUpdateDoc} variant="contained">Update</Button>
          </DialogActions>
        </Dialog>

        {/* Delete Confirmation Dialog */}
        <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
          <DialogTitle>Confirm Delete</DialogTitle>
          <DialogContent>
            <Typography>
              Are you sure you want to delete "{document?.title}"? This action cannot be undone.
            </Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
            <Button onClick={confirmDelete} color="error" variant="contained">
              Delete
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </motion.div>
  );
}

export default DocDetailPage;
