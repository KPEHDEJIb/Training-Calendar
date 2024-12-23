document.addEventListener("DOMContentLoaded", () => {
    const calendarEl = document.getElementById("calendar");
    const buttonStartEL = document.getElementById("buttonGotoStartWeek");
    const buttonEndEL = document.getElementById("buttonGotoEndWeek");
    const startDateEl = document.getElementById("startDate");
    const endDateEl = document.getElementById("endDate");

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        locale: "ru",
        firstDay: 1,
        events: [],
        eventContent: function (arg) {
            return {html: arg.event.title};
        },
        dateClick: function (arg) {
            const startMonday = getClickedWeekMonday(arg.dateStr).toISOString().split('T')[0];
            // alert(startMonday.toISOString().split('T')[0]);
            localStorage.setItem("startMonday", startMonday);
            loadExercises(startMonday);
        }
    });

    calendar.render();

    function getClickedWeekMonday(date) {
        const clickedDate = new Date(date);
        const day = clickedDate.getDay();
        const daysToMonday = (day === 0) ? -6 : 1 - day;
        clickedDate.setDate(clickedDate.getDate() + daysToMonday);
        return clickedDate;
    }

    function loadExercises(startMonday) {
        fetch(`/get_exercises/${startMonday}`)
            .then(response => response.json())
            .then(data => {
                calendar.removeAllEvents();
                calendar.addEventSource(data);
                gotoFirstWeek();
                updateStartEnd(startMonday);
            });
    }

    function gotoFirstWeek() {
        const startMonday = localStorage.getItem("startMonday");
        if (startMonday) {
            const endDate = new Date(startMonday);
            endDate.setDate(endDate.getDate() + 6);
            calendar.gotoDate(endDate.toISOString().split('T')[0]);
        }
    }

    function gotoLastWeek() {
        const startMonday = localStorage.getItem("startMonday");
        if (startMonday) {
            const endDate = new Date(startMonday);
            endDate.setDate(endDate.getDate() + 7 * 11 + 6);
            calendar.gotoDate(endDate.toISOString().split('T')[0]);
        }
    }

    function updateStartEnd(startMonday) {
        const endDate = new Date(startMonday);
        endDate.setDate(endDate.getDate() + 7 * 11 + 5);
        startDateEl.textContent = startMonday;
        endDateEl.textContent = endDate.toISOString().split('T')[0];
    }

    buttonStartEL.addEventListener("click", function () {
        gotoFirstWeek();
    });

    buttonEndEL.addEventListener("click", function () {
        gotoLastWeek();
    });

    const clickedDate = localStorage.getItem("startMonday");
    if (clickedDate) {
        loadExercises(clickedDate);
    }
});