import React from 'react'
import SocialLogin from './SocialLogin'
import CommenterAvatar from './CommenterAvatar'
import CreateUserForm from '../form/CreateUserForm'
import CommentForm from '../form/CommentForm'
const AuthenticateUser: React.FC = () => {
    return (
        <article className='display-form-and-comment-container'>
            <div className='comment-form-container'>
                <CommenterAvatar />
                <CommentForm />
            </div>
            <div className='login-user-container'>
                <div className='login-social-gosip-container'>
                    <SocialLogin />
                    <CreateUserForm />
                </div>
            </div>
        </article>

    )
}

export default AuthenticateUser