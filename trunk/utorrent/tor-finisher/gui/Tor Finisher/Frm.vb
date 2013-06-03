Public Class Frm

    Dim file As XDocument
    Dim settings As XElement

    Private Sub ClickLinkPynto(sender As Object, e As LinkLabelLinkClickedEventArgs) Handles lnkPynto.LinkClicked
        System.Diagnostics.Process.Start("http://pyntor.net16.net/")
    End Sub

    Private Sub ClickLinkDebora(sender As Object, e As LinkLabelLinkClickedEventArgs) Handles lblDebora.LinkClicked
        System.Diagnostics.Process.Start("http://www.facebook.com/DeboraaPereiraaa")
    End Sub

    Private Sub ClickLinkDonate(sender As Object, e As LinkLabelLinkClickedEventArgs) Handles lnkDonate.LinkClicked
        System.Diagnostics.Process.Start("https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=XGF8VS4RFTX2L")
    End Sub

    Private Sub ClickLinkContact(sender As Object, e As LinkLabelLinkClickedEventArgs) Handles lnkContact.LinkClicked
        System.Diagnostics.Process.Start("mailto:r.pynto@gmail.com")
    End Sub

    Private Sub ClickLinkSite(sender As Object, e As LinkLabelLinkClickedEventArgs) Handles lnkSite.LinkClicked
        System.Diagnostics.Process.Start("https://code.google.com/p/hautopc/")
    End Sub

    Private Sub ClickMoviesLocation(sender As Object, e As EventArgs) Handles cmdProcessingLibraryMovieslocation.Click
        If dlgFolder.ShowDialog() = Windows.Forms.DialogResult.OK Then
            txtProcessingLibraryMovieslocation.Text = dlgFolder.SelectedPath
        End If
    End Sub

    Private Sub ClickSeriesLocation(sender As Object, e As EventArgs) Handles cmdProcessingLibrarySerieslocation.Click
        If dlgFolder.ShowDialog() = Windows.Forms.DialogResult.OK Then
            txtProcessingLibrarySerieslocation.Text = dlgFolder.SelectedPath
        End If
    End Sub

    Private Sub ClickUnrarLocation(sender As Object, e As EventArgs) Handles cmdProcessingUnrarLocation.Click
        If dlgFile.ShowDialog() = Windows.Forms.DialogResult.OK Then
            txtProcessingUnrarLocation.Text = dlgFile.FileName
        End If
    End Sub

    Private Sub CheckEnable(sender As Object, e As EventArgs) Handles chkEnable.CheckedChanged
        For i As Integer = 0 To tabs.TabCount - 2
            tabs.TabPages(i).Enabled = chkEnable.Checked
        Next
    End Sub

    Private Sub CheckEmailEnable(sender As Object, e As EventArgs) Handles chkEmailEnable.CheckedChanged
        grpEmailHeaders.Enabled = chkEmailEnable.Checked
        grpEmailServer.Enabled = chkEmailEnable.Checked
    End Sub

    Private Sub CheckUtorrentEnablepause(sender As Object, e As EventArgs) Handles chkUtorrentEnablepause.CheckedChanged
        grpUtorrentServer.Enabled = chkUtorrentEnablepause.Checked Or chkUtorrentEnableremove.Checked
    End Sub

    Private Sub CheckUtorrentEnableremove(sender As Object, e As EventArgs) Handles chkUtorrentEnableremove.CheckedChanged
        grpUtorrentServer.Enabled = chkUtorrentEnablepause.Checked Or chkUtorrentEnableremove.Checked
    End Sub

    Private Sub CheckXbmcEnable(sender As Object, e As EventArgs) Handles chkXbmcEnable.CheckedChanged
        grpXbmcServer.Enabled = chkXbmcEnable.Checked
    End Sub

    Private Sub LoadValues()
        settings = file.Element("settings")

        chkEnable.Checked = Boolean.Parse(settings.<enabled>.Value)
        txtProcessingLibraryMovieslocation.Text = settings.<processing>.<library>.<movieslocation>.Value
        txtProcessingLibrarySerieslocation.Text = settings.<processing>.<library>.<serieslocation>.Value
        txtProcessingUtorrentMovieslabel.Text = settings.<processing>.<utorrent>.<movieslabel>.Value
        txtProcessingUtorrentSerieslabel.Text = settings.<processing>.<utorrent>.<serieslabel>.Value
        txtProcessingUtorrentLabelseparator.Text = settings.<processing>.<utorrent>.<labelseparator>.Value
        txtProcessingUnrarLocation.Text = settings.<processing>.<unrar>.<location>.Value
        chkProcessingLogEnable.Checked = Boolean.Parse(settings.<processing>.<log>.<enabled>.Value)
        chkEmailEnable.Checked = Boolean.Parse(settings.<email>.<enabled>.Value)
        txtEmailHeadersFrom.Text = settings.<email>.<headers>.<from>.Value
        txtEmailHeadersTo.Text = ""
        For i As Integer = 0 To settings.<email>.<headers>.<to>.<email>.Count - 1
            txtEmailHeadersTo.Text &= settings.<email>.<headers>.<to>.<email>(i).Value & vbCrLf
        Next
        txtEmailServerHost.Text = settings.<email>.<server>.<host>.Value
        txtEmailServerPort.Text = settings.<email>.<server>.<port>.Value
        txtEmailServerUsername.Text = settings.<email>.<server>.<username>.Value
        txtEmailServerPassword.Text = settings.<email>.<server>.<password>.Value
        chkUtorrentEnablepause.Checked = Boolean.Parse(settings.<utorrent>.<pauseenabled>.Value)
        chkUtorrentEnableremove.Checked = Boolean.Parse(settings.<utorrent>.<removeenabled>.Value)
        txtUtorrentServerHost.Text = settings.<utorrent>.<server>.<host>.Value
        txtUtorrentServerPort.Text = settings.<utorrent>.<server>.<port>.Value
        txtUtorrentServerUsername.Text = settings.<utorrent>.<server>.<username>.Value
        txtUtorrentServerPassword.Text = settings.<utorrent>.<server>.<password>.Value
        chkXbmcEnable.Checked = Boolean.Parse(settings.<xbmc>.<enabled>.Value)
        txtXbmcServerHost.Text = settings.<xbmc>.<server>.<host>.Value
        txtXbmcServerPort.Text = settings.<xbmc>.<server>.<port>.Value
        txtXbmcServerUsername.Text = settings.<xbmc>.<server>.<username>.Value
        txtXbmcServerPassword.Text = settings.<xbmc>.<server>.<password>.Value

        grpEmailHeaders.Enabled = chkEmailEnable.Checked
        grpEmailServer.Enabled = chkEmailEnable.Checked
        grpUtorrentServer.Enabled = chkUtorrentEnablepause.Checked Or chkUtorrentEnableremove.Checked
        grpXbmcServer.Enabled = chkXbmcEnable.Checked
        For i As Integer = 0 To tabs.TabCount - 2
            tabs.TabPages(i).Enabled = chkEnable.Checked
        Next

        If Boolean.Parse(settings.<firstrun>.Value) = True Then
            Dim ip As String = System.Net.Dns.GetHostByName(System.Net.Dns.GetHostName()).AddressList(0).ToString()
            txtUtorrentServerHost.Text = ip
            txtXbmcServerHost.Text = ip

            settings.<firstrun>.Value = Boolean.FalseString
            settings.<utorrent>.<server>.<host>.Value = ip
            settings.<xbmc>.<server>.<host>.Value = ip
            settings.<emailplay>.<server>.<host>.Value = ip
            file.Save(My.Application.Info.DirectoryPath & "\settings.xml")
        End If
    End Sub

    Private Sub SaveValues()
        settings.<enabled>.Value = chkEnable.Checked.ToString
        settings.<processing>.<library>.<movieslocation>.Value = txtProcessingLibraryMovieslocation.Text
        settings.<processing>.<library>.<serieslocation>.Value = txtProcessingLibrarySerieslocation.Text
        settings.<processing>.<utorrent>.<movieslabel>.Value = txtProcessingUtorrentMovieslabel.Text
        settings.<processing>.<utorrent>.<serieslabel>.Value = txtProcessingUtorrentSerieslabel.Text
        settings.<processing>.<utorrent>.<labelseparator>.Value = txtProcessingUtorrentLabelseparator.Text
        settings.<processing>.<unrar>.<location>.Value = txtProcessingUnrarLocation.Text
        settings.<processing>.<log>.<enabled>.Value = chkProcessingLogEnable.Checked.ToString
        settings.<email>.<enabled>.Value = chkEmailEnable.Checked.ToString
        settings.<email>.<headers>.<from>.Value = txtEmailHeadersFrom.Text
        Dim parent As XElement = settings.Element("email").Element("headers").Element("to")
        Dim child As XElement
        parent.RemoveNodes()
        For i As Integer = 0 To txtEmailHeadersTo.Lines.Count - 1
            If txtEmailHeadersTo.Lines(i).Length > 0 Then
                child = New XElement("email")
                child.Value = txtEmailHeadersTo.Lines(i)
                parent.Add(child)
            End If
        Next
        settings.<email>.<server>.<host>.Value = txtEmailServerHost.Text
        settings.<email>.<server>.<port>.Value = txtEmailServerPort.Text
        settings.<email>.<server>.<username>.Value = txtEmailServerUsername.Text
        settings.<email>.<server>.<password>.Value = txtEmailServerPassword.Text
        settings.<utorrent>.<pauseenabled>.Value = chkUtorrentEnablepause.Checked.ToString
        settings.<utorrent>.<removeenabled>.Value = chkUtorrentEnableremove.Checked.ToString
        settings.<utorrent>.<server>.<host>.Value = txtUtorrentServerHost.Text
        settings.<utorrent>.<server>.<port>.Value = txtUtorrentServerPort.Text
        settings.<utorrent>.<server>.<username>.Value = txtUtorrentServerUsername.Text
        settings.<utorrent>.<server>.<password>.Value = txtUtorrentServerPassword.Text
        settings.<xbmc>.<enabled>.Value = chkXbmcEnable.Checked.ToString
        settings.<xbmc>.<server>.<host>.Value = txtXbmcServerHost.Text
        settings.<xbmc>.<server>.<port>.Value = txtXbmcServerPort.Text
        settings.<xbmc>.<server>.<username>.Value = txtXbmcServerUsername.Text
        settings.<xbmc>.<server>.<password>.Value = txtXbmcServerPassword.Text
        file.Save(My.Application.Info.DirectoryPath & "\settings.xml")
    End Sub

    Private Sub Iniciate(sender As Object, e As EventArgs) Handles MyBase.Load
        file = XDocument.Load(My.Application.Info.DirectoryPath & "\settings.xml")
    End Sub

    Private Sub Iniciated() Handles MyBase.Shown
        Me.Hide()
    End Sub

    Private Sub ClickTray(sender As Object, e As MouseEventArgs) Handles trayIcon.MouseClick
        If Not Me.Visible Then
            LoadValues()
            Me.Show()
        End If
        Me.WindowState = FormWindowState.Normal
        Me.Activate()
        Me.tabs.Focus()
    End Sub

    Private Sub ClickSave(sender As Object, e As EventArgs) Handles cmdSave.Click
        SaveValues()
        Me.Hide()
    End Sub

    Private Sub ClickClose(sender As Object, e As FormClosingEventArgs) Handles MyBase.FormClosing
        e.Cancel = True
        Me.Hide()
    End Sub
End Class
