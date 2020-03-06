import axios from 'axios'
export default {
    state: {
        session: {
            token: localStorage.getItem('token') || null,
            message: ""
        },
    },
    mutations: {
        SetSession(state, session) {
            state.session = session
        }
    },
    actions: {
        async RetriveToken(ctx, credential) {
            console.log(credential);
            return new Promise((resolve, reject) =>

                axios.post('/login', {
                    username: credential.login,
                    password: credential.password
                })
                    .then(response => {
                        const token = response.data.token;
                        ctx.commit('SetSession', { token: token });
                        localStorage.setItem('token', token)
                        resolve(response.data.message)
                    })
                    .catch(error => reject(error))
            )
        }
    },
    getters: {
        isSessionValid: state => state.session.token
    },
}