import express from 'express';
import User from '../models/User.js';
import { v4 as uuidv4 } from 'uuid';

const router = express.Router();