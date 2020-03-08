import axios from 'axios'

if (localStorage.getItem('token'))
    axios.defaults.headers.common["Bearer"] = localStorage.getItem('token')
export default {
    namespaced: true,
    state: {
        token: localStorage.getItem('token') || null
    },
    mutations: {
        SetSession(state, session) {
            localStorage.setItem('token', session.token)
            state.token = session.token
            axios.defaults.headers.common["Bearer"] = state.token
        },
        DestroySession(state) {
            localStorage.removeItem('token')
            state.token = null
        }
    },
    actions: {
        async RetriveToken(ctx, credential) {
            return new Promise((resolve, reject) =>
                axios.post('/login', {
                    username: credential.login,
                    password: credential.password
                })
                    .then(response => {
                        ctx.commit('SetSession', { token: response.data.token });
                        resolve(response.data.message)
                    })
                    .catch(error => {
                        reject(error);
                    })
            )
        },
        async DestroyToken(ctx) {
            ctx.commit('DestroySession')
        }
    },
    getters: {
        isValid: state => state.token !== null,
        token: state => state.token,
    },
}