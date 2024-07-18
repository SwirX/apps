async function fetchApps() {
    const response = await fetch('apps/apps.json');
    const apps = await response.json();
    displayApps(apps);
}

function displayApps(apps) {
    const appsList = document.getElementById('apps-list');
    appsList.innerHTML = ''; // Clear previous content

    for (const [appName, appFiles] of Object.entries(apps)) {
        const appElement = document.createElement('div');
        appElement.classList.add('release');

        const appTitle = document.createElement('h2');
        appTitle.textContent = appName;
        appElement.appendChild(appTitle);

        const filesList = document.createElement('ul');
        appFiles.forEach(file => {
            const fileItem = document.createElement('li');
            const fileLink = document.createElement('a');
            fileLink.href = `apps/${appName}/${file}`;
            fileLink.textContent = file;
            fileItem.appendChild(fileLink);
            filesList.appendChild(fileItem);
        });

        appElement.appendChild(filesList);
        appsList.appendChild(appElement);
    }
}

fetchApps();
