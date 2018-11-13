var minutesLabel = document.getElementById("minutes");
var secondsLabel = document.getElementById("seconds");

var Clock = {
    totalSeconds: 0,

    start: function () {
        var self = this;
        function pad(val) { return val > 9 ? val : "0" + val; }
        this.interval = setInterval(function () {
            self.totalSeconds += 1;

            minutesLabel.innerHTML = pad(Math.floor(self.totalSeconds / 60 % 60));
            secondsLabel.innerHTML = pad(parseInt(self.totalSeconds % 60));
        }, 1000);
    },

    reset: function () {
        Clock.totalSeconds = null;
        clearInterval(this.interval);
        minutesLabel.innerHTML = "00";
        secondsLabel.innerHTML = "00";
    },

    pause: function () {
        clearInterval(this.interval);
        delete this.interval;
    },

    resume: function () {
        if (!this.interval) this.start();
    },

    restart: function () {
        this.reset();
        Clock.start();
    }
};

const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('start') !== null) {
    Clock.start();
}
else {
    Clock.pause();
}