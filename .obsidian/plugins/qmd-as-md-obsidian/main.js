'use strict';

var obsidian = require('obsidian');
var child_process = require('child_process');
var path = require('path');

function _interopNamespaceDefault(e) {
    var n = Object.create(null);
    if (e) {
        Object.keys(e).forEach(function (k) {
            if (k !== 'default') {
                var d = Object.getOwnPropertyDescriptor(e, k);
                Object.defineProperty(n, k, d.get ? d : {
                    enumerable: true,
                    get: function () { return e[k]; }
                });
            }
        });
    }
    n.default = e;
    return Object.freeze(n);
}

var path__namespace = /*#__PURE__*/_interopNamespaceDefault(path);

const DEFAULT_SETTINGS = {
    quartoPath: 'quarto',
    enableQmdLinking: true,
    quartoTypst: '',
    emitCompilationLogs: true,
    openPdfInObsidian: false,
};
class QmdAsMdPlugin extends obsidian.Plugin {
    constructor() {
        super(...arguments);
        this.activePreviewProcesses = new Map();
    }
    async onload() {
        console.log('Plugin is loading...');
        try {
            await this.loadSettings();
            console.log('Settings loaded:', this.settings);
            if (this.settings.enableQmdLinking) {
                this.registerQmdExtension();
            }
            this.addSettingTab(new QmdSettingTab(this.app, this));
            console.log('Settings tab added successfully');
            this.addRibbonIcon('eye', 'Toggle Quarto Preview', async () => {
                const file = this.getActiveQuartoFile();
                if (file) {
                    console.log(`Toggling preview for: ${file.path}`);
                    await this.togglePreview(file);
                }
            });
            console.log('Ribbon icon added');
            this.addCommand({
                id: 'toggle-quarto-preview',
                name: 'Toggle Quarto Preview',
                callback: async () => {
                    const file = this.getActiveQuartoFile();
                    if (file) {
                        console.log(`Command: Toggling preview for ${file.path}`);
                        await this.togglePreview(file);
                    }
                },
                hotkeys: [{ modifiers: ['Ctrl', 'Shift'], key: 'p' }],
            });
            this.addRibbonIcon('file-output', 'Render Quarto to PDF', async () => {
                const file = this.getActiveQuartoFile();
                if (file)
                    await this.renderPdf(file);
            });
            this.registerRenderCommand('render-quarto-pdf', 'Render Quarto (use YAML format)');
            this.registerRenderCommand('render-quarto-pdf-typst', 'Render Quarto to PDF (Typst engine)', 'typst');
            this.registerRenderCommand('render-quarto-pdf-latex', 'Render Quarto to PDF (LaTeX engine)', 'pdf');
            console.log('Commands added');
        }
        catch (error) {
            console.error('Error loading plugin:', error);
            new obsidian.Notice('Failed to load QmdAsMdPlugin. Check the developer console for details.');
        }
    }
    onunload() {
        console.log('Plugin is unloading...');
        this.stopAllPreviews();
    }
    async loadSettings() {
        this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    }
    async saveSettings() {
        await this.saveData(this.settings);
    }
    isQuartoFile(file) {
        return file.extension === 'qmd';
    }
    getActiveQuartoFile() {
        const activeView = this.app.workspace.getActiveViewOfType(obsidian.MarkdownView);
        if (activeView?.file && this.isQuartoFile(activeView.file)) {
            return activeView.file;
        }
        new obsidian.Notice('Current file is not a Quarto document');
        return null;
    }
    getVaultFullPath(file) {
        const adapter = this.app.vault.adapter;
        if (adapter instanceof obsidian.FileSystemAdapter) {
            return adapter.getFullPath(file.path);
        }
        new obsidian.Notice('Vault is not on a local filesystem; cannot run Quarto.');
        return null;
    }
    pdfPathFor(qmdFile) {
        return qmdFile.path.replace(/\.qmd$/i, '.pdf');
    }
    registerRenderCommand(id, name, toFormat) {
        this.addCommand({
            id,
            name,
            icon: 'file-output',
            callback: async () => {
                const file = this.getActiveQuartoFile();
                if (file)
                    await this.renderPdf(file, toFormat);
            },
        });
    }
    registerQmdExtension() {
        console.log('Registering .qmd as markdown...');
        this.registerExtensions(['qmd'], 'markdown');
        console.log('.qmd registered as markdown');
    }
    async togglePreview(file) {
        if (this.activePreviewProcesses.has(file.path)) {
            await this.stopPreview(file);
        }
        else {
            await this.startPreview(file);
        }
    }
    async startPreview(file) {
        if (this.activePreviewProcesses.has(file.path)) {
            console.log(`Preview already running for: ${file.path}`);
            return; // Preview already running
        }
        try {
            const abstractFile = this.app.vault.getAbstractFileByPath(file.path);
            if (!abstractFile || !(abstractFile instanceof obsidian.TFile)) {
                new obsidian.Notice(`File ${file.path} not found`);
                return;
            }
            const filePath = this.getVaultFullPath(abstractFile);
            if (!filePath)
                return;
            const workingDir = path__namespace.dirname(filePath);
            console.log(`Resolved file path: ${filePath}`);
            console.log(`Working directory: ${workingDir}`);
            const envVars = {
                ...process.env,
            };
            if (this.settings.quartoTypst.trim()) {
                envVars.QUARTO_TYPST = this.settings.quartoTypst.trim();
                console.log(`QUARTO_TYPST set to: ${envVars.QUARTO_TYPST}`);
            }
            const quartoProcess = child_process.spawn(this.settings.quartoPath, ['preview', filePath], {
                cwd: workingDir,
                env: envVars,
            });
            let previewUrl = null;
            quartoProcess.stdout?.on('data', (data) => {
                const output = data.toString();
                if (this.settings.emitCompilationLogs) {
                    console.log(`Quarto Preview Output: ${output}`);
                }
                if (output.includes('Browse at')) {
                    const match = output.match(/Browse at\s+(http:\/\/[^\s]+)/);
                    if (match && match[1]) {
                        previewUrl = match[1];
                        new obsidian.Notice(`Preview available at ${previewUrl}`);
                        const leaf = this.app.workspace.getLeaf('tab');
                        leaf.setViewState({
                            type: 'webviewer',
                            active: true,
                            state: {
                                url: previewUrl,
                            },
                        });
                        this.app.workspace.revealLeaf(leaf);
                    }
                }
            });
            quartoProcess.stderr?.on('data', (data) => {
                if (this.settings.emitCompilationLogs) {
                    console.error(`Quarto Preview Error: ${data}`);
                }
            });
            quartoProcess.on('close', (code) => {
                if (code !== null && code !== 0) {
                    new obsidian.Notice(`Quarto preview process exited with code ${code}`);
                }
                this.activePreviewProcesses.delete(file.path);
            });
            this.activePreviewProcesses.set(file.path, quartoProcess);
            new obsidian.Notice('Quarto preview started');
        }
        catch (error) {
            console.error('Failed to start Quarto preview:', error);
            new obsidian.Notice('Failed to start Quarto preview');
        }
    }
    async stopPreview(file) {
        const quartoProcess = this.activePreviewProcesses.get(file.path);
        if (quartoProcess) {
            if (!quartoProcess.killed) {
                quartoProcess.kill();
            }
            this.activePreviewProcesses.delete(file.path);
            new obsidian.Notice('Quarto preview stopped');
        }
    }
    stopAllPreviews() {
        this.activePreviewProcesses.forEach((quartoProcess, filePath) => {
            if (!quartoProcess.killed) {
                quartoProcess.kill();
            }
            this.activePreviewProcesses.delete(filePath);
        });
        if (this.activePreviewProcesses.size > 0) {
            new obsidian.Notice('All Quarto previews stopped');
        }
    }
    async renderPdf(file, toFormat) {
        try {
            const abstractFile = this.app.vault.getAbstractFileByPath(file.path);
            if (!abstractFile || !(abstractFile instanceof obsidian.TFile)) {
                new obsidian.Notice(`File ${file.path} not found`);
                return;
            }
            const filePath = this.getVaultFullPath(abstractFile);
            if (!filePath)
                return;
            const workingDir = path__namespace.dirname(filePath);
            const envVars = { ...process.env };
            if (this.settings.quartoTypst.trim()) {
                envVars.QUARTO_TYPST = this.settings.quartoTypst.trim();
            }
            const engineLabel = toFormat === 'typst' ? 'Typst' : toFormat === 'pdf' ? 'LaTeX' : 'use YAML format';
            new obsidian.Notice(`Rendering Quarto (${engineLabel})...`);
            // Best-guess path used for the pre-render leaf-capture (so we can
            // reuse an existing PDF tab on recompile). The authoritative path
            // comes from quarto's "Output created:" stdout line, parsed below.
            const guessedPdfPath = this.pdfPathFor(file);
            const existingLeaf = this.app.workspace
                .getLeavesOfType('pdf')
                .find((l) => l.view?.file?.path === guessedPdfPath);
            const args = ['render', filePath];
            if (toFormat)
                args.push('--to', toFormat);
            const quartoProcess = child_process.spawn(this.settings.quartoPath, args, {
                cwd: workingDir,
                env: envVars,
            });
            let detectedOutputBasename = null;
            quartoProcess.stdout?.on('data', (data) => {
                const output = data.toString();
                if (this.settings.emitCompilationLogs) {
                    console.log(`Quarto Render Output: ${output}`);
                }
                const match = output.match(/Output created:\s*(.+?)\s*$/m);
                if (match) {
                    detectedOutputBasename = path__namespace.basename(match[1].trim());
                }
            });
            quartoProcess.stderr?.on('data', (data) => {
                if (this.settings.emitCompilationLogs) {
                    console.error(`Quarto Render Error: ${data.toString()}`);
                }
            });
            quartoProcess.on('close', async (code) => {
                if (code !== 0) {
                    new obsidian.Notice(`Quarto render failed (exit ${code}). Check console.`);
                    return;
                }
                const sourceDir = file.parent?.path ?? '';
                const outputVaultPath = detectedOutputBasename
                    ? (sourceDir ? `${sourceDir}/${detectedOutputBasename}` : detectedOutputBasename)
                    : guessedPdfPath;
                const outputTFile = await this.waitForVaultFile(outputVaultPath);
                if (!outputTFile) {
                    new obsidian.Notice(`Quarto rendered, but ${outputVaultPath} did not appear in the vault within the timeout. Check Quarto's output-dir or vault sync.`);
                    return;
                }
                const isPdf = outputVaultPath.toLowerCase().endsWith('.pdf');
                if (!this.settings.openPdfInObsidian || !isPdf) {
                    new obsidian.Notice(isPdf
                        ? `PDF rendered: ${outputVaultPath}`
                        : `Rendered: ${outputVaultPath} (Obsidian's built-in viewer only handles PDFs).`);
                    return;
                }
                try {
                    const leaf = existingLeaf?.parent != null
                        ? existingLeaf
                        : this.app.workspace.getLeaf('split', 'vertical');
                    await leaf.openFile(outputTFile, { active: false });
                    this.app.workspace.revealLeaf(leaf);
                    new obsidian.Notice(`Opened ${outputVaultPath}`);
                }
                catch (err) {
                    console.error('Failed to open PDF in Obsidian:', err);
                    new obsidian.Notice(`PDF rendered at ${outputVaultPath}, but Obsidian could not open it (no PDF viewer registered?).`);
                }
            });
        }
        catch (error) {
            console.error('Failed to render Quarto PDF:', error);
            new obsidian.Notice('Failed to render Quarto PDF');
        }
    }
    async waitForVaultFile(vaultPath, timeoutMs = 5000) {
        const start = Date.now();
        while (Date.now() - start < timeoutMs) {
            const f = this.app.vault.getAbstractFileByPath(vaultPath);
            if (f instanceof obsidian.TFile)
                return f;
            await new Promise((r) => setTimeout(r, 200));
        }
        return null;
    }
}
class QmdSettingTab extends obsidian.PluginSettingTab {
    constructor(app, plugin) {
        super(app, plugin);
        this.plugin = plugin;
    }
    display() {
        const { containerEl } = this;
        containerEl.empty();
        console.log('Rendering settings tab...');
        containerEl.createEl('h2', { text: 'Quarto Preview Settings' });
        new obsidian.Setting(containerEl)
            .setName('Quarto Path')
            .setDesc('Path to Quarto executable (e.g., quarto, /usr/local/bin/quarto)')
            .addText((text) => text
            .setPlaceholder('quarto')
            .setValue(this.plugin.settings.quartoPath)
            .onChange(async (value) => {
            console.log(`Quarto path changed to: ${value}`);
            this.plugin.settings.quartoPath = value;
            await this.plugin.saveSettings();
        }));
        new obsidian.Setting(containerEl)
            .setName('Enable Editing Quarto Files')
            .setDesc('By default, plugin allows editing .qmd files. Disable this feature if there is a conflict with .qmd editing enabled by another plugin')
            .addToggle((toggle) => toggle
            .setValue(this.plugin.settings.enableQmdLinking)
            .onChange(async (value) => {
            console.log(`Enable QMD Editing setting changed to: ${value}`);
            this.plugin.settings.enableQmdLinking = value;
            if (value) {
                this.plugin.registerQmdExtension();
            }
        }));
        new obsidian.Setting(containerEl)
            .setName('QUARTO_TYPST Variable')
            .setDesc('Define the QUARTO_TYPST environment variable (leave empty to unset)')
            .addText((text) => text
            .setPlaceholder('e.g., typst_path')
            .setValue(this.plugin.settings.quartoTypst)
            .onChange(async (value) => {
            console.log(`QUARTO_TYPST set to: ${value}`);
            this.plugin.settings.quartoTypst = value;
            await this.plugin.saveSettings();
        }));
        new obsidian.Setting(containerEl)
            .setName('Emit Compilation Logs')
            .setDesc('Toggle whether to emit detailed compilation logs in the console')
            .addToggle((toggle) => toggle
            .setValue(this.plugin.settings.emitCompilationLogs)
            .onChange(async (value) => {
            console.log(`Emit Compilation Logs set to: ${value}`);
            this.plugin.settings.emitCompilationLogs = value;
            await this.plugin.saveSettings();
        }));
        new obsidian.Setting(containerEl)
            .setName('Open Compiled PDF in Obsidian')
            .setDesc('When rendering to PDF, open the resulting file inside Obsidian using the built-in PDF viewer. The .qmd source must live in the vault so the rendered PDF is accessible.')
            .addToggle((toggle) => toggle
            .setValue(this.plugin.settings.openPdfInObsidian)
            .onChange(async (value) => {
            console.log(`Open PDF in Obsidian set to: ${value}`);
            this.plugin.settings.openPdfInObsidian = value;
            await this.plugin.saveSettings();
        }));
        console.log('Settings tab rendered successfully');
    }
}

module.exports = QmdAsMdPlugin;


/* nosourcemap */