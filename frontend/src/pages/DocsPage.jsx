import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import {
  Box, Typography, Paper, List, ListItem, ListItemText,
  CircularProgress, Divider, Chip, ListItemButton, IconButton,
  Menu, MenuItem, Dialog, DialogTitle, DialogContent,
  DialogActions, Button, TextField
} from '@mui/material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';
import DocsImage from '../assets/docs.png';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete'; 

const pageVariants = {
  initial: { opacity: 0, y: 20 },
  in: { opacity: 1, y: 0 },
  out: { opacity: 0, y: -20 },
};

function DocsPage() {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [docToDelete, setDocToDelete] = useState(null);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editTitle, setEditTitle] = useState('');
  const [editContent, setEditContent] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);

  const handleMenuClick = (event, doc) => {
    setAnchorEl(event.currentTarget);
    setSelectedDoc(doc);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedDoc(null);
  };

  const handleEdit = () => {
    setEditTitle(selectedDoc.title);
    setEditContent(selectedDoc.content || '');
    setEditDialogOpen(true);
    handleMenuClose();
  };

  const handleUpdateDoc = async () => {
    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.put(`http://localhost:5000/api/docs/${selectedDoc.id}`, 
        { 
          title: editTitle,
          content: editContent
        },
        { headers: { Authorization: `Bearer ${token}` }}
      );
      
      console.log('Update response:', response.status, response.data);
      
      if (response.status === 200) {
        // Update local state dengan data dari backend
        setDocuments(documents.map(doc => 
          doc.id === selectedDoc.id 
            ? { ...doc, title: editTitle, content: editContent }
            : doc
        ));
        
        setEditDialogOpen(false);
        setSelectedDoc(null);
        setError(''); // Clear any previous errors
        console.log('Document updated successfully');
      } else {
        setError(`Failed to update document: ${response.data?.error || 'Unknown error'}`);
      }
    } catch (err) {
      console.error('Update error:', err);
      setError(`Failed to update document: ${err.response?.data?.error || err.message || 'Network error'}`);
    }
  };

  const handleDelete = () => {
    setDocToDelete(selectedDoc);
    setDeleteDialogOpen(true);
    handleMenuClose();
  };

  const confirmDelete = async () => {
    if (!docToDelete?.id) {
      setError('No document selected for deletion');
      return;
    }

    try {
      const token = localStorage.getItem('authToken');
      const response = await axios.delete(`http://localhost:5000/api/docs/${docToDelete.id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (response.status === 200) {
        // Update local state - remove deleted document
        setDocuments(prevDocs => prevDocs.filter(doc => doc.id !== docToDelete.id));
        
        setDeleteDialogOpen(false);
        setDocToDelete(null);
        setError(''); // Clear any previous errors
        console.log('Document deleted successfully');
      } else {
        setError(`Failed to delete document: ${response.data?.error || 'Unknown error'}`);
      }
    } catch (err) {
      console.error('Delete error:', err);
      setError(`Failed to delete document: ${err.response?.data?.error || err.message || 'Network error'}`);
    }
  };

  useEffect(() => {
    const fetchDocs = async () => {
      try {
        const token = localStorage.getItem('authToken');
        const res = await axios.get('http://localhost:5000/api/docs', {
          headers: { Authorization: `Bearer ${token}` }
        });
        setDocuments(res.data);
      } catch (err) {
        setError('Failed to load documents.');
      } finally {
        setLoading(false);
      }
    };
    if (user) {
      fetchDocs();
    }
  }, [user]);

  if (loading) {
    return <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}><CircularProgress /></Box>;
  }

  if (error) {
    return <Typography color="error" sx={{ p: 3 }}>{error}</Typography>;
  }

  return (
    <motion.div initial="initial" animate="in" exit="out" variants={pageVariants}>
      <Box sx={{ p: { xs: 2, sm: 3 } }}>
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, alignItems: 'center', justifyContent: 'space-between', mb: 4, textAlign: { xs: 'center', md: 'left' } }}>
            <Box>
                <Typography variant="h1" gutterBottom>My Documents</Typography>
                <Typography variant="h5" color="text.secondary">
                A list of documents you have generated with AI.
                </Typography>
            </Box>
            <Box
                component="img"
                src={DocsImage}
                alt="Documents illustration"
                sx={{ height: { xs: 180, md: 220 }, maxWidth: { xs: '70%', md: 'auto' } }}
            />
        </Box>
        
        <Paper>
          <List>
            {documents.length > 0 ? (
              documents.map((doc, index) => (
                <React.Fragment key={doc.id}>
                  <ListItem 
                    disablePadding
                    secondaryAction={
                      <IconButton
                        edge="end"
                        onClick={(e) => handleMenuClick(e, doc)}
                      >
                        <MoreVertIcon />
                      </IconButton>
                    }
                  >
                    <ListItemButton onClick={() => navigate(`/docs/${doc.id}`)}>
                      <ListItemText
                        primary={doc.title}
                        secondary={
                          <Box component="span">
                            <Typography component="span" variant="body2" color="text.primary" display="block">
                              Created at: {new Date(doc.created_at).toLocaleString()}
                            </Typography>
                            <Box sx={{ mt: 1 }}>
                              <Chip label={doc.document_type} size="small" sx={{ mr: 1 }} />
                              <Chip label={doc.subject} size="small" />
                            </Box>
                          </Box>
                        }
                      />
                    </ListItemButton>
                  </ListItem>
                  {index < documents.length - 1 && <Divider component="li" />}
                </React.Fragment>
              ))
            ) : (
              <ListItem>
                <ListItemText primary="You don't have any saved documents yet." />
              </ListItem>
            )}
          </List>
        </Paper>

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
              placeholder="Enter your document content here..."
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
              Are you sure you want to delete "{docToDelete?.title}"? This action cannot be undone.
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

export default DocsPage;