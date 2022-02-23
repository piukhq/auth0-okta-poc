const oktaAuth = new OktaAuth({
    issuer: "https://bink.okta.com/oauth2/default",
    clientId: "0oah7yxtdugAD6cnd696",
    redirectUri: window.location.origin,
    postLogoutRedirectUri: window.location.origin
})

window.onload = async () => {
    updateUI()

    const isAuthed = await oktaAuth.isAuthenticated()
    if (isAuthed) return

    if (oktaAuth.isLoginRedirect()) {
        oktaAuth.setOriginalUri(window.location.origin)
        await oktaAuth.handleLoginRedirect()
    }
}

const updateUI = async () => {
    const isAuthed = await oktaAuth.isAuthenticated()

    el("btn-login").disabled = isAuthed
    el("btn-logout").disabled = !isAuthed

    let token = undefined
    if (isAuthed) {
        token = oktaAuth.getAccessToken()
    }

    if (isAuthed) {
        el("gated-content").classList.remove("hidden")

        el("ipt-access-token").textContent = token
        el("ipt-user-profile").textContent = JSON.stringify(await oktaAuth.getUser(), null, 4)
    } else {
        el("gated-content").classList.add("hidden")
    }

    el("status-public").textContent = await fetchEndpoint("/public")
    el("status-private").textContent = await fetchEndpoint("/private", token)
}

const login = () => {
    oktaAuth.signInWithRedirect()
}

const logout = () => {
    oktaAuth.signOut()
}

const fetchEndpoint = async (endpoint, token) => {
    const isAuthed = await oktaAuth.isAuthenticated()

    let headers = {}
    if (isAuthed && token) {
        headers["Authorization"] = `Bearer ${token}`
    }

    const url = `http://localhost:6502/api${endpoint}`
    return await fetch(url, {
        headers
    }).then(res => res.text()).catch(err => err)
}

const el = (id) => {
    return document.getElementById(id)
}
