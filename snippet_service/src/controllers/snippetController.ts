import { Response } from 'express';
import Snippet from '../models/Snippet';
import { AuthRequest } from '../middleware/auth';

// Crear un nuevo snippet
export const createSnippet = async (req: AuthRequest, res: Response) => {
    try {
        const { title, code, language, description, tags } = req.body;
        const userId = req.user.sub || req.user.identity; // Ajustar según el payload del token

        const newSnippet = new Snippet({
            title,
            code,
            language,
            description,
            tags,
            userId
        });

        const savedSnippet = await newSnippet.save();
        res.status(201).json(savedSnippet);
    } catch (error) {
        res.status(500).json({ error: (error as Error).message });
    }
};

// Obtener todos los snippets (del usuario autenticado)
export const getAllSnippets = async (req: AuthRequest, res: Response) => {
    try {
        const userId = req.user.sub || req.user.identity;
        const snippets = await Snippet.find({ userId }).sort({ createdAt: -1 });
        res.json(snippets);
    } catch (error) {
        res.status(500).json({ error: (error as Error).message });
    }
};

// Obtener un snippet por ID
export const getSnippetById = async (req: AuthRequest, res: Response) => {
    try {
        const snippet = await Snippet.findById(req.params.id);
        if (!snippet) {
            return res.status(404).json({ error: 'Snippet no encontrado' });
        }
        res.json(snippet);
    } catch (error) {
        res.status(500).json({ error: (error as Error).message });
    }
};

// Actualizar un snippet
export const updateSnippet = async (req: AuthRequest, res: Response) => {
    try {
        const { title, code, language, description, tags } = req.body;
        const snippet = await Snippet.findByIdAndUpdate(
            req.params.id,
            { title, code, language, description, tags },
            { new: true }
        );
        if (!snippet) {
            return res.status(404).json({ error: 'Snippet no encontrado' });
        }
        res.json(snippet);
    } catch (error) {
        res.status(500).json({ error: (error as Error).message });
    }
};

// Eliminar un snippet
export const deleteSnippet = async (req: AuthRequest, res: Response) => {
    try {
        const snippet = await Snippet.findByIdAndDelete(req.params.id);
        if (!snippet) {
            return res.status(404).json({ error: 'Snippet no encontrado' });
        }
        res.json({ message: 'Snippet eliminado correctamente' });
    } catch (error) {
        res.status(500).json({ error: (error as Error).message });
    }
};
