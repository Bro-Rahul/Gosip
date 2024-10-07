import React from 'react'
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z, ZodType } from 'zod';


const CommentForm: React.FC = () => {
    type CommentBody = {
        body: string;
    };

    const schema: ZodType<CommentBody> = z.object({
        body: z.string().min(3, "Comment must be at least 3 characters long")
    });

    const { register, handleSubmit, formState: { errors }, reset } = useForm<CommentBody>({
        resolver: zodResolver(schema)
    });

    const onSubmit = (data: CommentBody) => {
        console.log(data)
        reset()
    };

    return (
        <form className='comment-form' onSubmit={handleSubmit(onSubmit)}>
            <div>
                <textarea className='textarea' placeholder='Join The Discussion...'  {...register('body')}></textarea>
                <p className='error'>{errors.body?.message}</p>
            </div>
            <div>
                <button className='comment-btn'>Comment</button>
            </div>
        </form>
    );
}

export default CommentForm;