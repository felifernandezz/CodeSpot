import mongoose, { Document, Schema } from 'mongoose';

export interface ISnippet extends Document {
    title: string;
    code: string;
    language: string;
    description?: string;
    createdAt: Date;
}

const SnippetSchema: Schema = new Schema({
    title: { type: String, required: true },
    code: { type: String, required: true },
    language: { type: String, required: true },
    description: { type: String },
    createdAt: { type: Date, default: Date.now },
});

export default mongoose.model<ISnippet>('Snippet', SnippetSchema);
