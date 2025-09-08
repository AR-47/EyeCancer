import express from 'express';
import User from '../models/User.js';
import { v4 as uuidv4 } from 'uuid';

const router = express.Router();

router.post('/form', async (req, res) => {
  try {
    const userData = req.body;

    userData.patientId = uuidv4();

    const user = await User.create(userData);
    
    res.status(201).json({
      success: true,
      message: 'User registered successfully',
      patientId: user.patientId,
      user
    });
  }