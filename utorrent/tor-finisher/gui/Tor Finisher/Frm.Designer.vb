<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class Frm
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        Me.components = New System.ComponentModel.Container()
        Dim resources As System.ComponentModel.ComponentResourceManager = New System.ComponentModel.ComponentResourceManager(GetType(Frm))
        Me.cmdSave = New System.Windows.Forms.Button()
        Me.chkEnable = New System.Windows.Forms.CheckBox()
        Me.tabs = New System.Windows.Forms.TabControl()
        Me.tabProcessing = New System.Windows.Forms.TabPage()
        Me.grpProcessingLog = New System.Windows.Forms.GroupBox()
        Me.chkProcessingLogEnable = New System.Windows.Forms.CheckBox()
        Me.grpProcessingUnrar = New System.Windows.Forms.GroupBox()
        Me.cmdProcessingUnrarLocation = New System.Windows.Forms.Button()
        Me.txtProcessingUnrarLocation = New System.Windows.Forms.TextBox()
        Me.lblProcessingUnrarLocation = New System.Windows.Forms.Label()
        Me.grpProcessingUtorrent = New System.Windows.Forms.GroupBox()
        Me.txtProcessingUtorrentLabelseparator = New System.Windows.Forms.TextBox()
        Me.lblProcessingUtorrentLabelseparator = New System.Windows.Forms.Label()
        Me.txtProcessingUtorrentSerieslabel = New System.Windows.Forms.TextBox()
        Me.lblProcessingUtorrentSerieslabel = New System.Windows.Forms.Label()
        Me.txtProcessingUtorrentMovieslabel = New System.Windows.Forms.TextBox()
        Me.lblProcessingUtorrentMovieslabel = New System.Windows.Forms.Label()
        Me.grpProcessingLibrary = New System.Windows.Forms.GroupBox()
        Me.lblProcessingLibraryMovieslocation = New System.Windows.Forms.Label()
        Me.cmdProcessingLibraryMovieslocation = New System.Windows.Forms.Button()
        Me.txtProcessingLibraryMovieslocation = New System.Windows.Forms.TextBox()
        Me.txtProcessingLibrarySerieslocation = New System.Windows.Forms.TextBox()
        Me.lblProcessingLibrarySerieslocation = New System.Windows.Forms.Label()
        Me.cmdProcessingLibrarySerieslocation = New System.Windows.Forms.Button()
        Me.tabEmail = New System.Windows.Forms.TabPage()
        Me.grpEmailHeaders = New System.Windows.Forms.GroupBox()
        Me.lblEmailHeadersTo = New System.Windows.Forms.Label()
        Me.txtEmailHeadersTo = New System.Windows.Forms.TextBox()
        Me.txtEmailHeadersFrom = New System.Windows.Forms.TextBox()
        Me.lblEmailHeadersFrom = New System.Windows.Forms.Label()
        Me.grpEmailServer = New System.Windows.Forms.GroupBox()
        Me.txtEmailServerPassword = New System.Windows.Forms.TextBox()
        Me.lblEmailServerPassword = New System.Windows.Forms.Label()
        Me.txtEmailServerUsername = New System.Windows.Forms.TextBox()
        Me.lblEmailServerUsername = New System.Windows.Forms.Label()
        Me.txtEmailServerPort = New System.Windows.Forms.TextBox()
        Me.lblEmailServerPort = New System.Windows.Forms.Label()
        Me.txtEmailServerHost = New System.Windows.Forms.TextBox()
        Me.lblEmailServerHost = New System.Windows.Forms.Label()
        Me.chkEmailEnable = New System.Windows.Forms.CheckBox()
        Me.tabUtorrent = New System.Windows.Forms.TabPage()
        Me.grpUtorrentServer = New System.Windows.Forms.GroupBox()
        Me.txtUtorrentServerPassword = New System.Windows.Forms.TextBox()
        Me.lblUtorrentServerPassword = New System.Windows.Forms.Label()
        Me.txtUtorrentServerUsername = New System.Windows.Forms.TextBox()
        Me.lblUtorrentServerUsername = New System.Windows.Forms.Label()
        Me.txtUtorrentServerPort = New System.Windows.Forms.TextBox()
        Me.lblUtorrentServerPort = New System.Windows.Forms.Label()
        Me.txtUtorrentServerHost = New System.Windows.Forms.TextBox()
        Me.lblUtorrentServerHost = New System.Windows.Forms.Label()
        Me.chkUtorrentEnableremove = New System.Windows.Forms.CheckBox()
        Me.chkUtorrentEnablepause = New System.Windows.Forms.CheckBox()
        Me.tabXbmc = New System.Windows.Forms.TabPage()
        Me.grpXbmcServer = New System.Windows.Forms.GroupBox()
        Me.txtXbmcServerPassword = New System.Windows.Forms.TextBox()
        Me.lblXbmcServerPassword = New System.Windows.Forms.Label()
        Me.txtXbmcServerUsername = New System.Windows.Forms.TextBox()
        Me.lblXbmcServerUsername = New System.Windows.Forms.Label()
        Me.txtXbmcServerPort = New System.Windows.Forms.TextBox()
        Me.lblXbmcServerPort = New System.Windows.Forms.Label()
        Me.txtXbmcServerHost = New System.Windows.Forms.TextBox()
        Me.lblXbmcServerHost = New System.Windows.Forms.Label()
        Me.chkXbmcEnable = New System.Windows.Forms.CheckBox()
        Me.tabAbout = New System.Windows.Forms.TabPage()
        Me.Panel1 = New System.Windows.Forms.Panel()
        Me.lblDebora = New System.Windows.Forms.LinkLabel()
        Me.lblLogo = New System.Windows.Forms.Label()
        Me.imgLogo = New System.Windows.Forms.PictureBox()
        Me.lblVersion = New System.Windows.Forms.Label()
        Me.lblTitle = New System.Windows.Forms.Label()
        Me.lnkPynto = New System.Windows.Forms.LinkLabel()
        Me.lblCreated = New System.Windows.Forms.Label()
        Me.lnkContact = New System.Windows.Forms.LinkLabel()
        Me.lnkDonate = New System.Windows.Forms.LinkLabel()
        Me.lnkSite = New System.Windows.Forms.LinkLabel()
        Me.dlgFolder = New System.Windows.Forms.FolderBrowserDialog()
        Me.dlgFile = New System.Windows.Forms.OpenFileDialog()
        Me.trayIcon = New System.Windows.Forms.NotifyIcon(Me.components)
        Me.tabs.SuspendLayout()
        Me.tabProcessing.SuspendLayout()
        Me.grpProcessingLog.SuspendLayout()
        Me.grpProcessingUnrar.SuspendLayout()
        Me.grpProcessingUtorrent.SuspendLayout()
        Me.grpProcessingLibrary.SuspendLayout()
        Me.tabEmail.SuspendLayout()
        Me.grpEmailHeaders.SuspendLayout()
        Me.grpEmailServer.SuspendLayout()
        Me.tabUtorrent.SuspendLayout()
        Me.grpUtorrentServer.SuspendLayout()
        Me.tabXbmc.SuspendLayout()
        Me.grpXbmcServer.SuspendLayout()
        Me.tabAbout.SuspendLayout()
        Me.Panel1.SuspendLayout()
        CType(Me.imgLogo, System.ComponentModel.ISupportInitialize).BeginInit()
        Me.SuspendLayout()
        '
        'cmdSave
        '
        resources.ApplyResources(Me.cmdSave, "cmdSave")
        Me.cmdSave.Name = "cmdSave"
        Me.cmdSave.UseVisualStyleBackColor = True
        '
        'chkEnable
        '
        resources.ApplyResources(Me.chkEnable, "chkEnable")
        Me.chkEnable.Name = "chkEnable"
        Me.chkEnable.UseVisualStyleBackColor = True
        '
        'tabs
        '
        resources.ApplyResources(Me.tabs, "tabs")
        Me.tabs.Controls.Add(Me.tabProcessing)
        Me.tabs.Controls.Add(Me.tabEmail)
        Me.tabs.Controls.Add(Me.tabUtorrent)
        Me.tabs.Controls.Add(Me.tabXbmc)
        Me.tabs.Controls.Add(Me.tabAbout)
        Me.tabs.Name = "tabs"
        Me.tabs.SelectedIndex = 0
        '
        'tabProcessing
        '
        Me.tabProcessing.BackColor = System.Drawing.SystemColors.Control
        Me.tabProcessing.Controls.Add(Me.grpProcessingLog)
        Me.tabProcessing.Controls.Add(Me.grpProcessingUnrar)
        Me.tabProcessing.Controls.Add(Me.grpProcessingUtorrent)
        Me.tabProcessing.Controls.Add(Me.grpProcessingLibrary)
        resources.ApplyResources(Me.tabProcessing, "tabProcessing")
        Me.tabProcessing.Name = "tabProcessing"
        '
        'grpProcessingLog
        '
        resources.ApplyResources(Me.grpProcessingLog, "grpProcessingLog")
        Me.grpProcessingLog.Controls.Add(Me.chkProcessingLogEnable)
        Me.grpProcessingLog.Name = "grpProcessingLog"
        Me.grpProcessingLog.TabStop = False
        '
        'chkProcessingLogEnable
        '
        resources.ApplyResources(Me.chkProcessingLogEnable, "chkProcessingLogEnable")
        Me.chkProcessingLogEnable.Name = "chkProcessingLogEnable"
        Me.chkProcessingLogEnable.UseVisualStyleBackColor = True
        '
        'grpProcessingUnrar
        '
        resources.ApplyResources(Me.grpProcessingUnrar, "grpProcessingUnrar")
        Me.grpProcessingUnrar.Controls.Add(Me.cmdProcessingUnrarLocation)
        Me.grpProcessingUnrar.Controls.Add(Me.txtProcessingUnrarLocation)
        Me.grpProcessingUnrar.Controls.Add(Me.lblProcessingUnrarLocation)
        Me.grpProcessingUnrar.Name = "grpProcessingUnrar"
        Me.grpProcessingUnrar.TabStop = False
        '
        'cmdProcessingUnrarLocation
        '
        resources.ApplyResources(Me.cmdProcessingUnrarLocation, "cmdProcessingUnrarLocation")
        Me.cmdProcessingUnrarLocation.Name = "cmdProcessingUnrarLocation"
        Me.cmdProcessingUnrarLocation.UseVisualStyleBackColor = True
        '
        'txtProcessingUnrarLocation
        '
        resources.ApplyResources(Me.txtProcessingUnrarLocation, "txtProcessingUnrarLocation")
        Me.txtProcessingUnrarLocation.Name = "txtProcessingUnrarLocation"
        '
        'lblProcessingUnrarLocation
        '
        resources.ApplyResources(Me.lblProcessingUnrarLocation, "lblProcessingUnrarLocation")
        Me.lblProcessingUnrarLocation.Name = "lblProcessingUnrarLocation"
        '
        'grpProcessingUtorrent
        '
        resources.ApplyResources(Me.grpProcessingUtorrent, "grpProcessingUtorrent")
        Me.grpProcessingUtorrent.Controls.Add(Me.txtProcessingUtorrentLabelseparator)
        Me.grpProcessingUtorrent.Controls.Add(Me.lblProcessingUtorrentLabelseparator)
        Me.grpProcessingUtorrent.Controls.Add(Me.txtProcessingUtorrentSerieslabel)
        Me.grpProcessingUtorrent.Controls.Add(Me.lblProcessingUtorrentSerieslabel)
        Me.grpProcessingUtorrent.Controls.Add(Me.txtProcessingUtorrentMovieslabel)
        Me.grpProcessingUtorrent.Controls.Add(Me.lblProcessingUtorrentMovieslabel)
        Me.grpProcessingUtorrent.Name = "grpProcessingUtorrent"
        Me.grpProcessingUtorrent.TabStop = False
        '
        'txtProcessingUtorrentLabelseparator
        '
        resources.ApplyResources(Me.txtProcessingUtorrentLabelseparator, "txtProcessingUtorrentLabelseparator")
        Me.txtProcessingUtorrentLabelseparator.Name = "txtProcessingUtorrentLabelseparator"
        '
        'lblProcessingUtorrentLabelseparator
        '
        resources.ApplyResources(Me.lblProcessingUtorrentLabelseparator, "lblProcessingUtorrentLabelseparator")
        Me.lblProcessingUtorrentLabelseparator.Name = "lblProcessingUtorrentLabelseparator"
        '
        'txtProcessingUtorrentSerieslabel
        '
        resources.ApplyResources(Me.txtProcessingUtorrentSerieslabel, "txtProcessingUtorrentSerieslabel")
        Me.txtProcessingUtorrentSerieslabel.Name = "txtProcessingUtorrentSerieslabel"
        '
        'lblProcessingUtorrentSerieslabel
        '
        resources.ApplyResources(Me.lblProcessingUtorrentSerieslabel, "lblProcessingUtorrentSerieslabel")
        Me.lblProcessingUtorrentSerieslabel.Name = "lblProcessingUtorrentSerieslabel"
        '
        'txtProcessingUtorrentMovieslabel
        '
        resources.ApplyResources(Me.txtProcessingUtorrentMovieslabel, "txtProcessingUtorrentMovieslabel")
        Me.txtProcessingUtorrentMovieslabel.Name = "txtProcessingUtorrentMovieslabel"
        '
        'lblProcessingUtorrentMovieslabel
        '
        resources.ApplyResources(Me.lblProcessingUtorrentMovieslabel, "lblProcessingUtorrentMovieslabel")
        Me.lblProcessingUtorrentMovieslabel.Name = "lblProcessingUtorrentMovieslabel"
        '
        'grpProcessingLibrary
        '
        resources.ApplyResources(Me.grpProcessingLibrary, "grpProcessingLibrary")
        Me.grpProcessingLibrary.Controls.Add(Me.lblProcessingLibraryMovieslocation)
        Me.grpProcessingLibrary.Controls.Add(Me.cmdProcessingLibraryMovieslocation)
        Me.grpProcessingLibrary.Controls.Add(Me.txtProcessingLibraryMovieslocation)
        Me.grpProcessingLibrary.Controls.Add(Me.txtProcessingLibrarySerieslocation)
        Me.grpProcessingLibrary.Controls.Add(Me.lblProcessingLibrarySerieslocation)
        Me.grpProcessingLibrary.Controls.Add(Me.cmdProcessingLibrarySerieslocation)
        Me.grpProcessingLibrary.Name = "grpProcessingLibrary"
        Me.grpProcessingLibrary.TabStop = False
        '
        'lblProcessingLibraryMovieslocation
        '
        resources.ApplyResources(Me.lblProcessingLibraryMovieslocation, "lblProcessingLibraryMovieslocation")
        Me.lblProcessingLibraryMovieslocation.Name = "lblProcessingLibraryMovieslocation"
        '
        'cmdProcessingLibraryMovieslocation
        '
        resources.ApplyResources(Me.cmdProcessingLibraryMovieslocation, "cmdProcessingLibraryMovieslocation")
        Me.cmdProcessingLibraryMovieslocation.Name = "cmdProcessingLibraryMovieslocation"
        Me.cmdProcessingLibraryMovieslocation.UseVisualStyleBackColor = True
        '
        'txtProcessingLibraryMovieslocation
        '
        resources.ApplyResources(Me.txtProcessingLibraryMovieslocation, "txtProcessingLibraryMovieslocation")
        Me.txtProcessingLibraryMovieslocation.Name = "txtProcessingLibraryMovieslocation"
        '
        'txtProcessingLibrarySerieslocation
        '
        resources.ApplyResources(Me.txtProcessingLibrarySerieslocation, "txtProcessingLibrarySerieslocation")
        Me.txtProcessingLibrarySerieslocation.Name = "txtProcessingLibrarySerieslocation"
        '
        'lblProcessingLibrarySerieslocation
        '
        resources.ApplyResources(Me.lblProcessingLibrarySerieslocation, "lblProcessingLibrarySerieslocation")
        Me.lblProcessingLibrarySerieslocation.Name = "lblProcessingLibrarySerieslocation"
        '
        'cmdProcessingLibrarySerieslocation
        '
        resources.ApplyResources(Me.cmdProcessingLibrarySerieslocation, "cmdProcessingLibrarySerieslocation")
        Me.cmdProcessingLibrarySerieslocation.Name = "cmdProcessingLibrarySerieslocation"
        Me.cmdProcessingLibrarySerieslocation.UseVisualStyleBackColor = True
        '
        'tabEmail
        '
        Me.tabEmail.BackColor = System.Drawing.SystemColors.Control
        Me.tabEmail.Controls.Add(Me.grpEmailHeaders)
        Me.tabEmail.Controls.Add(Me.grpEmailServer)
        Me.tabEmail.Controls.Add(Me.chkEmailEnable)
        resources.ApplyResources(Me.tabEmail, "tabEmail")
        Me.tabEmail.Name = "tabEmail"
        '
        'grpEmailHeaders
        '
        resources.ApplyResources(Me.grpEmailHeaders, "grpEmailHeaders")
        Me.grpEmailHeaders.Controls.Add(Me.lblEmailHeadersTo)
        Me.grpEmailHeaders.Controls.Add(Me.txtEmailHeadersTo)
        Me.grpEmailHeaders.Controls.Add(Me.txtEmailHeadersFrom)
        Me.grpEmailHeaders.Controls.Add(Me.lblEmailHeadersFrom)
        Me.grpEmailHeaders.Name = "grpEmailHeaders"
        Me.grpEmailHeaders.TabStop = False
        '
        'lblEmailHeadersTo
        '
        resources.ApplyResources(Me.lblEmailHeadersTo, "lblEmailHeadersTo")
        Me.lblEmailHeadersTo.Name = "lblEmailHeadersTo"
        '
        'txtEmailHeadersTo
        '
        Me.txtEmailHeadersTo.AcceptsReturn = True
        resources.ApplyResources(Me.txtEmailHeadersTo, "txtEmailHeadersTo")
        Me.txtEmailHeadersTo.Name = "txtEmailHeadersTo"
        '
        'txtEmailHeadersFrom
        '
        resources.ApplyResources(Me.txtEmailHeadersFrom, "txtEmailHeadersFrom")
        Me.txtEmailHeadersFrom.Name = "txtEmailHeadersFrom"
        '
        'lblEmailHeadersFrom
        '
        resources.ApplyResources(Me.lblEmailHeadersFrom, "lblEmailHeadersFrom")
        Me.lblEmailHeadersFrom.Name = "lblEmailHeadersFrom"
        '
        'grpEmailServer
        '
        resources.ApplyResources(Me.grpEmailServer, "grpEmailServer")
        Me.grpEmailServer.Controls.Add(Me.txtEmailServerPassword)
        Me.grpEmailServer.Controls.Add(Me.lblEmailServerPassword)
        Me.grpEmailServer.Controls.Add(Me.txtEmailServerUsername)
        Me.grpEmailServer.Controls.Add(Me.lblEmailServerUsername)
        Me.grpEmailServer.Controls.Add(Me.txtEmailServerPort)
        Me.grpEmailServer.Controls.Add(Me.lblEmailServerPort)
        Me.grpEmailServer.Controls.Add(Me.txtEmailServerHost)
        Me.grpEmailServer.Controls.Add(Me.lblEmailServerHost)
        Me.grpEmailServer.Name = "grpEmailServer"
        Me.grpEmailServer.TabStop = False
        '
        'txtEmailServerPassword
        '
        resources.ApplyResources(Me.txtEmailServerPassword, "txtEmailServerPassword")
        Me.txtEmailServerPassword.Name = "txtEmailServerPassword"
        Me.txtEmailServerPassword.UseSystemPasswordChar = True
        '
        'lblEmailServerPassword
        '
        resources.ApplyResources(Me.lblEmailServerPassword, "lblEmailServerPassword")
        Me.lblEmailServerPassword.Name = "lblEmailServerPassword"
        '
        'txtEmailServerUsername
        '
        resources.ApplyResources(Me.txtEmailServerUsername, "txtEmailServerUsername")
        Me.txtEmailServerUsername.Name = "txtEmailServerUsername"
        '
        'lblEmailServerUsername
        '
        resources.ApplyResources(Me.lblEmailServerUsername, "lblEmailServerUsername")
        Me.lblEmailServerUsername.Name = "lblEmailServerUsername"
        '
        'txtEmailServerPort
        '
        resources.ApplyResources(Me.txtEmailServerPort, "txtEmailServerPort")
        Me.txtEmailServerPort.Name = "txtEmailServerPort"
        '
        'lblEmailServerPort
        '
        resources.ApplyResources(Me.lblEmailServerPort, "lblEmailServerPort")
        Me.lblEmailServerPort.Name = "lblEmailServerPort"
        '
        'txtEmailServerHost
        '
        resources.ApplyResources(Me.txtEmailServerHost, "txtEmailServerHost")
        Me.txtEmailServerHost.Name = "txtEmailServerHost"
        '
        'lblEmailServerHost
        '
        resources.ApplyResources(Me.lblEmailServerHost, "lblEmailServerHost")
        Me.lblEmailServerHost.Name = "lblEmailServerHost"
        '
        'chkEmailEnable
        '
        resources.ApplyResources(Me.chkEmailEnable, "chkEmailEnable")
        Me.chkEmailEnable.Name = "chkEmailEnable"
        Me.chkEmailEnable.UseVisualStyleBackColor = True
        '
        'tabUtorrent
        '
        Me.tabUtorrent.BackColor = System.Drawing.SystemColors.Control
        Me.tabUtorrent.Controls.Add(Me.grpUtorrentServer)
        Me.tabUtorrent.Controls.Add(Me.chkUtorrentEnableremove)
        Me.tabUtorrent.Controls.Add(Me.chkUtorrentEnablepause)
        resources.ApplyResources(Me.tabUtorrent, "tabUtorrent")
        Me.tabUtorrent.Name = "tabUtorrent"
        '
        'grpUtorrentServer
        '
        resources.ApplyResources(Me.grpUtorrentServer, "grpUtorrentServer")
        Me.grpUtorrentServer.Controls.Add(Me.txtUtorrentServerPassword)
        Me.grpUtorrentServer.Controls.Add(Me.lblUtorrentServerPassword)
        Me.grpUtorrentServer.Controls.Add(Me.txtUtorrentServerUsername)
        Me.grpUtorrentServer.Controls.Add(Me.lblUtorrentServerUsername)
        Me.grpUtorrentServer.Controls.Add(Me.txtUtorrentServerPort)
        Me.grpUtorrentServer.Controls.Add(Me.lblUtorrentServerPort)
        Me.grpUtorrentServer.Controls.Add(Me.txtUtorrentServerHost)
        Me.grpUtorrentServer.Controls.Add(Me.lblUtorrentServerHost)
        Me.grpUtorrentServer.Name = "grpUtorrentServer"
        Me.grpUtorrentServer.TabStop = False
        '
        'txtUtorrentServerPassword
        '
        resources.ApplyResources(Me.txtUtorrentServerPassword, "txtUtorrentServerPassword")
        Me.txtUtorrentServerPassword.Name = "txtUtorrentServerPassword"
        Me.txtUtorrentServerPassword.UseSystemPasswordChar = True
        '
        'lblUtorrentServerPassword
        '
        resources.ApplyResources(Me.lblUtorrentServerPassword, "lblUtorrentServerPassword")
        Me.lblUtorrentServerPassword.Name = "lblUtorrentServerPassword"
        '
        'txtUtorrentServerUsername
        '
        resources.ApplyResources(Me.txtUtorrentServerUsername, "txtUtorrentServerUsername")
        Me.txtUtorrentServerUsername.Name = "txtUtorrentServerUsername"
        '
        'lblUtorrentServerUsername
        '
        resources.ApplyResources(Me.lblUtorrentServerUsername, "lblUtorrentServerUsername")
        Me.lblUtorrentServerUsername.Name = "lblUtorrentServerUsername"
        '
        'txtUtorrentServerPort
        '
        resources.ApplyResources(Me.txtUtorrentServerPort, "txtUtorrentServerPort")
        Me.txtUtorrentServerPort.Name = "txtUtorrentServerPort"
        '
        'lblUtorrentServerPort
        '
        resources.ApplyResources(Me.lblUtorrentServerPort, "lblUtorrentServerPort")
        Me.lblUtorrentServerPort.Name = "lblUtorrentServerPort"
        '
        'txtUtorrentServerHost
        '
        resources.ApplyResources(Me.txtUtorrentServerHost, "txtUtorrentServerHost")
        Me.txtUtorrentServerHost.Name = "txtUtorrentServerHost"
        '
        'lblUtorrentServerHost
        '
        resources.ApplyResources(Me.lblUtorrentServerHost, "lblUtorrentServerHost")
        Me.lblUtorrentServerHost.Name = "lblUtorrentServerHost"
        '
        'chkUtorrentEnableremove
        '
        resources.ApplyResources(Me.chkUtorrentEnableremove, "chkUtorrentEnableremove")
        Me.chkUtorrentEnableremove.Name = "chkUtorrentEnableremove"
        Me.chkUtorrentEnableremove.UseVisualStyleBackColor = True
        '
        'chkUtorrentEnablepause
        '
        resources.ApplyResources(Me.chkUtorrentEnablepause, "chkUtorrentEnablepause")
        Me.chkUtorrentEnablepause.Name = "chkUtorrentEnablepause"
        Me.chkUtorrentEnablepause.UseVisualStyleBackColor = True
        '
        'tabXbmc
        '
        Me.tabXbmc.BackColor = System.Drawing.SystemColors.Control
        Me.tabXbmc.Controls.Add(Me.grpXbmcServer)
        Me.tabXbmc.Controls.Add(Me.chkXbmcEnable)
        resources.ApplyResources(Me.tabXbmc, "tabXbmc")
        Me.tabXbmc.Name = "tabXbmc"
        '
        'grpXbmcServer
        '
        resources.ApplyResources(Me.grpXbmcServer, "grpXbmcServer")
        Me.grpXbmcServer.Controls.Add(Me.txtXbmcServerPassword)
        Me.grpXbmcServer.Controls.Add(Me.lblXbmcServerPassword)
        Me.grpXbmcServer.Controls.Add(Me.txtXbmcServerUsername)
        Me.grpXbmcServer.Controls.Add(Me.lblXbmcServerUsername)
        Me.grpXbmcServer.Controls.Add(Me.txtXbmcServerPort)
        Me.grpXbmcServer.Controls.Add(Me.lblXbmcServerPort)
        Me.grpXbmcServer.Controls.Add(Me.txtXbmcServerHost)
        Me.grpXbmcServer.Controls.Add(Me.lblXbmcServerHost)
        Me.grpXbmcServer.Name = "grpXbmcServer"
        Me.grpXbmcServer.TabStop = False
        '
        'txtXbmcServerPassword
        '
        resources.ApplyResources(Me.txtXbmcServerPassword, "txtXbmcServerPassword")
        Me.txtXbmcServerPassword.Name = "txtXbmcServerPassword"
        Me.txtXbmcServerPassword.UseSystemPasswordChar = True
        '
        'lblXbmcServerPassword
        '
        resources.ApplyResources(Me.lblXbmcServerPassword, "lblXbmcServerPassword")
        Me.lblXbmcServerPassword.Name = "lblXbmcServerPassword"
        '
        'txtXbmcServerUsername
        '
        resources.ApplyResources(Me.txtXbmcServerUsername, "txtXbmcServerUsername")
        Me.txtXbmcServerUsername.Name = "txtXbmcServerUsername"
        '
        'lblXbmcServerUsername
        '
        resources.ApplyResources(Me.lblXbmcServerUsername, "lblXbmcServerUsername")
        Me.lblXbmcServerUsername.Name = "lblXbmcServerUsername"
        '
        'txtXbmcServerPort
        '
        resources.ApplyResources(Me.txtXbmcServerPort, "txtXbmcServerPort")
        Me.txtXbmcServerPort.Name = "txtXbmcServerPort"
        '
        'lblXbmcServerPort
        '
        resources.ApplyResources(Me.lblXbmcServerPort, "lblXbmcServerPort")
        Me.lblXbmcServerPort.Name = "lblXbmcServerPort"
        '
        'txtXbmcServerHost
        '
        resources.ApplyResources(Me.txtXbmcServerHost, "txtXbmcServerHost")
        Me.txtXbmcServerHost.Name = "txtXbmcServerHost"
        '
        'lblXbmcServerHost
        '
        resources.ApplyResources(Me.lblXbmcServerHost, "lblXbmcServerHost")
        Me.lblXbmcServerHost.Name = "lblXbmcServerHost"
        '
        'chkXbmcEnable
        '
        resources.ApplyResources(Me.chkXbmcEnable, "chkXbmcEnable")
        Me.chkXbmcEnable.Name = "chkXbmcEnable"
        Me.chkXbmcEnable.UseVisualStyleBackColor = True
        '
        'tabAbout
        '
        Me.tabAbout.BackColor = System.Drawing.SystemColors.Control
        Me.tabAbout.Controls.Add(Me.Panel1)
        Me.tabAbout.Controls.Add(Me.lnkContact)
        Me.tabAbout.Controls.Add(Me.lnkDonate)
        Me.tabAbout.Controls.Add(Me.lnkSite)
        resources.ApplyResources(Me.tabAbout, "tabAbout")
        Me.tabAbout.Name = "tabAbout"
        '
        'Panel1
        '
        resources.ApplyResources(Me.Panel1, "Panel1")
        Me.Panel1.Controls.Add(Me.lblDebora)
        Me.Panel1.Controls.Add(Me.lblLogo)
        Me.Panel1.Controls.Add(Me.imgLogo)
        Me.Panel1.Controls.Add(Me.lblVersion)
        Me.Panel1.Controls.Add(Me.lblTitle)
        Me.Panel1.Controls.Add(Me.lnkPynto)
        Me.Panel1.Controls.Add(Me.lblCreated)
        Me.Panel1.Name = "Panel1"
        '
        'lblDebora
        '
        resources.ApplyResources(Me.lblDebora, "lblDebora")
        Me.lblDebora.Name = "lblDebora"
        Me.lblDebora.TabStop = True
        '
        'lblLogo
        '
        resources.ApplyResources(Me.lblLogo, "lblLogo")
        Me.lblLogo.Name = "lblLogo"
        '
        'imgLogo
        '
        resources.ApplyResources(Me.imgLogo, "imgLogo")
        Me.imgLogo.Name = "imgLogo"
        Me.imgLogo.TabStop = False
        '
        'lblVersion
        '
        resources.ApplyResources(Me.lblVersion, "lblVersion")
        Me.lblVersion.Name = "lblVersion"
        '
        'lblTitle
        '
        resources.ApplyResources(Me.lblTitle, "lblTitle")
        Me.lblTitle.Name = "lblTitle"
        '
        'lnkPynto
        '
        resources.ApplyResources(Me.lnkPynto, "lnkPynto")
        Me.lnkPynto.Name = "lnkPynto"
        Me.lnkPynto.TabStop = True
        '
        'lblCreated
        '
        resources.ApplyResources(Me.lblCreated, "lblCreated")
        Me.lblCreated.Name = "lblCreated"
        '
        'lnkContact
        '
        resources.ApplyResources(Me.lnkContact, "lnkContact")
        Me.lnkContact.Name = "lnkContact"
        Me.lnkContact.TabStop = True
        '
        'lnkDonate
        '
        resources.ApplyResources(Me.lnkDonate, "lnkDonate")
        Me.lnkDonate.Name = "lnkDonate"
        Me.lnkDonate.TabStop = True
        '
        'lnkSite
        '
        resources.ApplyResources(Me.lnkSite, "lnkSite")
        Me.lnkSite.Name = "lnkSite"
        Me.lnkSite.TabStop = True
        '
        'dlgFolder
        '
        Me.dlgFolder.RootFolder = System.Environment.SpecialFolder.MyComputer
        '
        'dlgFile
        '
        Me.dlgFile.FileName = "UnRAR.exe"
        resources.ApplyResources(Me.dlgFile, "dlgFile")
        Me.dlgFile.InitialDirectory = "C:\Program Files\WinRAR"
        '
        'trayIcon
        '
        resources.ApplyResources(Me.trayIcon, "trayIcon")
        '
        'Frm
        '
        Me.AcceptButton = Me.cmdSave
        resources.ApplyResources(Me, "$this")
        Me.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
        Me.Controls.Add(Me.tabs)
        Me.Controls.Add(Me.chkEnable)
        Me.Controls.Add(Me.cmdSave)
        Me.Name = "Frm"
        Me.tabs.ResumeLayout(False)
        Me.tabProcessing.ResumeLayout(False)
        Me.grpProcessingLog.ResumeLayout(False)
        Me.grpProcessingLog.PerformLayout()
        Me.grpProcessingUnrar.ResumeLayout(False)
        Me.grpProcessingUnrar.PerformLayout()
        Me.grpProcessingUtorrent.ResumeLayout(False)
        Me.grpProcessingUtorrent.PerformLayout()
        Me.grpProcessingLibrary.ResumeLayout(False)
        Me.grpProcessingLibrary.PerformLayout()
        Me.tabEmail.ResumeLayout(False)
        Me.tabEmail.PerformLayout()
        Me.grpEmailHeaders.ResumeLayout(False)
        Me.grpEmailHeaders.PerformLayout()
        Me.grpEmailServer.ResumeLayout(False)
        Me.grpEmailServer.PerformLayout()
        Me.tabUtorrent.ResumeLayout(False)
        Me.tabUtorrent.PerformLayout()
        Me.grpUtorrentServer.ResumeLayout(False)
        Me.grpUtorrentServer.PerformLayout()
        Me.tabXbmc.ResumeLayout(False)
        Me.tabXbmc.PerformLayout()
        Me.grpXbmcServer.ResumeLayout(False)
        Me.grpXbmcServer.PerformLayout()
        Me.tabAbout.ResumeLayout(False)
        Me.Panel1.ResumeLayout(False)
        Me.Panel1.PerformLayout()
        CType(Me.imgLogo, System.ComponentModel.ISupportInitialize).EndInit()
        Me.ResumeLayout(False)
        Me.PerformLayout()

    End Sub
    Friend WithEvents cmdSave As System.Windows.Forms.Button
    Friend WithEvents chkEnable As System.Windows.Forms.CheckBox
    Friend WithEvents tabs As System.Windows.Forms.TabControl
    Friend WithEvents tabProcessing As System.Windows.Forms.TabPage
    Friend WithEvents lblProcessingLibraryMovieslocation As System.Windows.Forms.Label
    Friend WithEvents tabEmail As System.Windows.Forms.TabPage
    Friend WithEvents txtProcessingLibraryMovieslocation As System.Windows.Forms.TextBox
    Friend WithEvents cmdProcessingLibraryMovieslocation As System.Windows.Forms.Button
    Friend WithEvents dlgFolder As System.Windows.Forms.FolderBrowserDialog
    Friend WithEvents txtProcessingLibrarySerieslocation As System.Windows.Forms.TextBox
    Friend WithEvents cmdProcessingLibrarySerieslocation As System.Windows.Forms.Button
    Friend WithEvents lnkSite As System.Windows.Forms.LinkLabel
    Friend WithEvents txtEmailHeadersFrom As System.Windows.Forms.TextBox
    Friend WithEvents lblEmailHeadersFrom As System.Windows.Forms.Label
    Friend WithEvents lblProcessingUnrarLocation As System.Windows.Forms.Label
    Friend WithEvents cmdProcessingUnrarLocation As System.Windows.Forms.Button
    Friend WithEvents txtProcessingUnrarLocation As System.Windows.Forms.TextBox
    Friend WithEvents grpProcessingLibrary As System.Windows.Forms.GroupBox
    Friend WithEvents grpProcessingLog As System.Windows.Forms.GroupBox
    Friend WithEvents chkProcessingLogEnable As System.Windows.Forms.CheckBox
    Friend WithEvents grpProcessingUnrar As System.Windows.Forms.GroupBox
    Friend WithEvents grpProcessingUtorrent As System.Windows.Forms.GroupBox
    Friend WithEvents txtProcessingUtorrentLabelseparator As System.Windows.Forms.TextBox
    Friend WithEvents lblProcessingUtorrentLabelseparator As System.Windows.Forms.Label
    Friend WithEvents txtProcessingUtorrentSerieslabel As System.Windows.Forms.TextBox
    Friend WithEvents lblProcessingUtorrentSerieslabel As System.Windows.Forms.Label
    Friend WithEvents txtProcessingUtorrentMovieslabel As System.Windows.Forms.TextBox
    Friend WithEvents lblProcessingUtorrentMovieslabel As System.Windows.Forms.Label
    Friend WithEvents grpEmailHeaders As System.Windows.Forms.GroupBox
    Friend WithEvents grpEmailServer As System.Windows.Forms.GroupBox
    Friend WithEvents txtEmailServerPassword As System.Windows.Forms.TextBox
    Friend WithEvents lblEmailServerPassword As System.Windows.Forms.Label
    Friend WithEvents txtEmailServerUsername As System.Windows.Forms.TextBox
    Friend WithEvents lblEmailServerUsername As System.Windows.Forms.Label
    Friend WithEvents txtEmailServerPort As System.Windows.Forms.TextBox
    Friend WithEvents lblEmailServerPort As System.Windows.Forms.Label
    Friend WithEvents txtEmailServerHost As System.Windows.Forms.TextBox
    Friend WithEvents lblEmailServerHost As System.Windows.Forms.Label
    Friend WithEvents chkEmailEnable As System.Windows.Forms.CheckBox
    Friend WithEvents lblEmailHeadersTo As System.Windows.Forms.Label
    Friend WithEvents txtEmailHeadersTo As System.Windows.Forms.TextBox
    Friend WithEvents tabUtorrent As System.Windows.Forms.TabPage
    Friend WithEvents tabXbmc As System.Windows.Forms.TabPage
    Friend WithEvents chkUtorrentEnableremove As System.Windows.Forms.CheckBox
    Friend WithEvents chkUtorrentEnablepause As System.Windows.Forms.CheckBox
    Friend WithEvents chkXbmcEnable As System.Windows.Forms.CheckBox
    Friend WithEvents dlgFile As System.Windows.Forms.OpenFileDialog
    Friend WithEvents lblProcessingLibrarySerieslocation As System.Windows.Forms.Label
    Friend WithEvents grpUtorrentServer As System.Windows.Forms.GroupBox
    Friend WithEvents txtUtorrentServerPassword As System.Windows.Forms.TextBox
    Friend WithEvents lblUtorrentServerPassword As System.Windows.Forms.Label
    Friend WithEvents txtUtorrentServerUsername As System.Windows.Forms.TextBox
    Friend WithEvents lblUtorrentServerUsername As System.Windows.Forms.Label
    Friend WithEvents txtUtorrentServerPort As System.Windows.Forms.TextBox
    Friend WithEvents lblUtorrentServerPort As System.Windows.Forms.Label
    Friend WithEvents txtUtorrentServerHost As System.Windows.Forms.TextBox
    Friend WithEvents lblUtorrentServerHost As System.Windows.Forms.Label
    Friend WithEvents grpXbmcServer As System.Windows.Forms.GroupBox
    Friend WithEvents txtXbmcServerPassword As System.Windows.Forms.TextBox
    Friend WithEvents lblXbmcServerPassword As System.Windows.Forms.Label
    Friend WithEvents txtXbmcServerUsername As System.Windows.Forms.TextBox
    Friend WithEvents lblXbmcServerUsername As System.Windows.Forms.Label
    Friend WithEvents txtXbmcServerPort As System.Windows.Forms.TextBox
    Friend WithEvents lblXbmcServerPort As System.Windows.Forms.Label
    Friend WithEvents txtXbmcServerHost As System.Windows.Forms.TextBox
    Friend WithEvents lblXbmcServerHost As System.Windows.Forms.Label
    Friend WithEvents tabAbout As System.Windows.Forms.TabPage
    Friend WithEvents lblVersion As System.Windows.Forms.Label
    Friend WithEvents imgLogo As System.Windows.Forms.PictureBox
    Friend WithEvents lnkContact As System.Windows.Forms.LinkLabel
    Friend WithEvents lnkDonate As System.Windows.Forms.LinkLabel
    Friend WithEvents lnkPynto As System.Windows.Forms.LinkLabel
    Friend WithEvents lblCreated As System.Windows.Forms.Label
    Friend WithEvents lblTitle As System.Windows.Forms.Label
    Friend WithEvents trayIcon As System.Windows.Forms.NotifyIcon
    Friend WithEvents Panel1 As System.Windows.Forms.Panel
    Friend WithEvents lblDebora As System.Windows.Forms.LinkLabel
    Friend WithEvents lblLogo As System.Windows.Forms.Label

End Class
