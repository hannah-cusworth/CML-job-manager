function change_status(idnum)
    {
        event.stopPropagation();
        var info = {"idnum": idnum};
        var row = document.getElementById(idnum);
        var url = document.getElementById("url").textContent;
        row.style.display = "none";
        url.replace('/','');
        print(url);
        $.ajax(
                {
                    url: url,
                    type: "post",
                    data: info,
                    headers: {'X-CSRFToken': '{{ csrf_token }}'}, 
                });
    }