function exit() {
    document.getElementById("bod").innerHTML = `
        <table align="center">
            <tr>
                <td style="text-align: center;">
                    <img style="max-width: 160px; max-height: 200px;" src="https://ryanchausse.com/logo/unisi_logo.jpg" alt="University of Siena logo" />
                    <h1 style="margin: 0.0px 0.0px 16.1px 0.0px; text-align: center; line-height: 28.0px; font: 24.0px Times; color: #000000; -webkit-text-stroke: #000000">
                        <span class="s1">Exited the Experiment</span>
                    </h1>
                    <p>
                        Your information has been discarded.
                    </p>
                    <p>
                        If you have any questions, please contact Aubrie Amstutz at aubrie.amstutz@student.unisi.it
                    </p>
                    <a href="#" onClick="window.location.href = './experiment.html';" style="text-decoration: none; color: blue;">Start Over</a>
                </td>
            </tr>
        </table>
    `;
//  window.location.href = './exit.html'
}