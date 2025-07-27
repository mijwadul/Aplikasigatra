import React, { useState } from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField, FormControl, InputLabel, Select, MenuItem, FormHelperText } from '@mui/material';

function UserFormModal({ open, onClose, onSubmit, formData, setFormData, initialData = {} }) {
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    const { confirmPassword, ...submissionData } = formData;
    onSubmit(submissionData);
  };

  return (
    <Dialog open={open} onClose={onClose} component="form" onSubmit={handleSubmit} fullWidth maxWidth="xs">
      <DialogTitle>{initialData.id ? 'Edit User' : 'Add New User'}</DialogTitle>
      <DialogContent>
        {/* TextFields and Select components remain the same */}
        <TextField autoFocus margin="dense" name="username" label="Username" fullWidth value={formData.username} onChange={handleChange} required />
        <TextField margin="dense" name="email" label="Email Address" type="email" fullWidth value={formData.email} onChange={handleChange} required />
        <TextField
          margin="dense"
          name="password"
          label="Password"
          type="password"
          fullWidth
          value={formData.password}
          onChange={handleChange}
          required={!initialData.id}
          helperText={initialData.id ? "Leave blank to keep current password" : ""}
        />
        <TextField
          margin="dense"
          name="confirmPassword"
          label="Confirm Password"
          type="password"
          fullWidth
          value={formData.confirmPassword}
          onChange={handleChange}
          required={!initialData.id || !!formData.password}
          error={!!error}
        />
        <FormControl fullWidth margin="dense" required>
          <InputLabel>Role</InputLabel>
          <Select name="role" value={formData.role} label="Role" onChange={handleChange}>
            <MenuItem value="Teacher">Teacher</MenuItem>
            <MenuItem value="School Admin">School Admin</MenuItem>
            <MenuItem value="Developer">Developer</MenuItem>
          </Select>
        </FormControl>
        {error && <FormHelperText error sx={{ mt: 1 }}>{error}</FormHelperText>}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button type="submit" variant="contained">
          {initialData.id ? 'Confirm' : 'Create User'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default UserFormModal;