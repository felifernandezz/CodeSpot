import express, { Request, Response } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { connectDB } from './db';
import snippetRoutes from './routes/snippetRoutes';

dotenv.config();

const app = express();
const port = process.env.PORT || 8080;

app.use(cors());
app.use(express.json());

connectDB();

app.use('/snippets', snippetRoutes);

app.get('/db', (req: Request, res: Response) => {
    res.json({ message: '¡El servicio de Snippets (Node.js + Mongo) está funcionando!' });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});