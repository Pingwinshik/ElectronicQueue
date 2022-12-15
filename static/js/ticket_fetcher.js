fetch("ticket.json")
        .then((response) => response.json())
        .then((data) => {
          for (var i = 0; i < data.items.length; i++) {
            let vnumber = data.items[i].number;
            let vroom = data.items[i].room;
            let vtime = data.items[i].time;
            let vdate = data.items[i].date;
            let vdocs = data.items[i].docs;
            document.querySelector("#number").innerHTML += `${vnumber}`;
            document.querySelector("#room").innerHTML += `${vroom}`;
            document.querySelector("#time").innerHTML += `${vtime}`;
            document.querySelector("#date").innerHTML += `${vdate}`;
            document.querySelector("#docs").innerHTML += `${vdocs}`;
          }
        });
