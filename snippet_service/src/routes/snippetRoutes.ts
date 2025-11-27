import { Router } from 'express';
import { authenticateToken } from '../middleware/auth';
import {
    createSnippet,
    getAllSnippets,
    getSnippetById,
    updateSnippet,
    deleteSnippet
} from '../controllers/snippetController';

const router = Router();

// Todas las rutas requieren autenticación
router.use(authenticateToken);

router.post('/', createSnippet);
router.get('/', getAllSnippets);
router.get('/:id', getSnippetById);
router.put('/:id', updateSnippet);
router.delete('/:id', deleteSnippet);

export default router;
