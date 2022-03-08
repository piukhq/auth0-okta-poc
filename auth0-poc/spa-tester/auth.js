let auth0 = null

const configureClient = async () => {
    auth0 = await createAuth0Client({
        domain: "dev-s-2ims9r.eu.auth0.com",
        client_id: "eLDoDIawgDOqaracZz8DuzNkIeykbqzf",
        audience: "https://quickstart/api",
        scope: "read:mids write:mids"
    })
}

window.onload = async () => {
    await configureClient()

    updateUI()

    const isAuthed = await auth0.isAuthenticated()
    if (isAuthed) return

    const query = window.location.search
    if (query.includes("error=")) {
        el("error-message").classList.remove("hidden")
        el("error-message-text").textContent = qsVar("error_description")
    } else if (query.includes("code=") && query.includes("state=")) {
        await auth0.handleRedirectCallback()
        updateUI()
        window.history.replaceState({}, document.title, "/")
    }
}

const updateUI = async () => {
    const isAuthed = await auth0.isAuthenticated()

    el("btn-login").disabled = isAuthed
    el("btn-logout").disabled = !isAuthed

    let token = undefined
    if (isAuthed) {
        token = await auth0.getTokenSilently()
    }

    if (isAuthed) {
        el("gated-content").classList.remove("hidden")

        el("access-token").textContent = token
        el("user-profile").textContent = JSON.stringify(await auth0.getUser(), null, 4)
    } else {
        el("gated-content").classList.add("hidden")
    }

    el("status-public").textContent = await fetchEndpoint("/public")
    el("status-read-mids").textContent = await fetchEndpoint("/read-mids", token)
    el("status-write-mids").textContent = await fetchEndpoint("/write-mids", token)
}

const login = async () => {
    await auth0.loginWithRedirect({
        redirect_uri: window.location.origin
    })
}

const logout = async () => {
    auth0.logout({
        returnTo: window.location.origin
    })
}

const fetchEndpoint = async (endpoint, token) => {
    const isAuthed = await auth0.isAuthenticated()

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

const qsVar = (variable) => {
    var query = window.location.search.substring(1)
    var vars = query.split("&")
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=")
        if (pair[0] == variable) {
            return decodeURIComponent(pair[1])
        }
    }
    return false
}