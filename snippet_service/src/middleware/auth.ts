import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

// Extendemos la interfaz de Request para incluir el usuario
export interface AuthRequest extends Request {
    user?: any;
}

export const authenticateToken = (req: AuthRequest, res: Response, next: NextFunction) => {
    const authHeader = req.headers['authorization'];
    // El header viene como "Bearer <token>"
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: 'Acceso denegado: Token no proporcionado' });
    }

    // La misma clave secreta que usamos en Flask
    const secret = process.env.JWT_SECRET_KEY || 'super-secret-key-project';

    jwt.verify(token, secret, (err: any, user: any) => {
        if (err) {
            return res.status(403).json({ error: 'Token inválido o expirado' });
        }
        // "user" aquí es el payload del token (que contiene "sub" o "identity" con el ID)
        req.user = user;
        next();
    });
};
