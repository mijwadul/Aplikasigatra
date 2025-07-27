import React, { useState, useEffect, useContext } from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import AuthContext from '../../context/AuthContext';

function ClassFormModal({ open, onClose, onSubmit, schools = [], initialData = {} }) {
  const { user } = useContext(AuthContext);
  const [formData, setFormData] = useState({ name: '', grade_level: '', school_id: '' });

  useEffect(() => {
    // This effect runs when the modal is opened to set the form's initial state
    if (open) {
      setFormData({
        name: initialData.name || '',
        grade_level: initialData.grade_level || '',
        // For Admins, school_id is their own. For Developers, it's whatever is passed in or empty.
        school_id: initialData.school_id || (user?.role === 'School Admin' ? user.school_id : ''),
      });
    }
  }, [initialData, open, user]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Dialog open={open} onClose={onClose} component="form" onSubmit={handleSubmit} fullWidth maxWidth="xs">
      <DialogTitle>{initialData.id ? 'Edit Class' : 'Add New Class'}</DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          margin="dense"
          name="name"
          label="Class Name"
          fullWidth
          variant="outlined"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <TextField
          margin="dense"
          name="grade_level"
          label="Grade Level (e.g., 7, 8, 9)"
          fullWidth
          variant="outlined"
          value={formData.grade_level}
          onChange={handleChange}
          required
        />
        
        {/* Only show the School selector to Developers */}
        {user?.role === 'Developer' && (
          <FormControl fullWidth margin="dense" required>
            <InputLabel>School</InputLabel>
            <Select
              name="school_id"
              value={formData.school_id}
              label="School"
              onChange={handleChange}
            >
              {schools.map(school => (
                <MenuItem key={school.id} value={school.id}>{school.name}</MenuItem>
              ))}
            </Select>
          </FormControl>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button type="submit" variant="contained">{initialData.id ? 'Save Changes' : 'Create Class'}</Button>
      </DialogActions>
    </Dialog>
  );
}

export default ClassFormModal;