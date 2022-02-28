var length = title.length;
var title_hidden = "";
var missed = 0;

for(i=0; i<length; i++)
{
    if(title.charAt(i)==" ")title_hidden = title_hidden + " ";
    else title_hidden = title_hidden + "-";
}

function refresh_title()
{
    document.getElementById("title").innerHTML = title_hidden
}

function start()
{
    var alphabet_div = ""

    for(i=0;i<=35;i++)
    {
        if(i<=25)
        {
            var elem = "letter" + (65 + i);
            alphabet_div = alphabet_div + '<div class="letter" onclick="check('+(65+i)+')" id="'+elem+'">'+String.fromCharCode(65 + i)+'</div>';
        }
        else
        {
            var elem = "letter" + (22+ i);
            alphabet_div = alphabet_div + '<div class="letter" onclick="check('+(22+i)+')" id="'+elem+'">'+String.fromCharCode(48 + i - 26)+'</div>';
        }
        if((i+1)%6 == 0)alphabet_div = alphabet_div + '<div style="clear:both;"></div>'
    }
    document.getElementById("alphabet").innerHTML = alphabet_div;
    refresh_title()
}

String.prototype.changeLetter = function (index, letter)
{
    if(index > this.length-1) return this.toString();
    else return this.substr(0, index) + letter + this.substr(index+1);

}

function check(number)
{
    var correct = false;

    for(i=0;i<length;i++)
    {
        if(title.charAt(i)==String.fromCharCode(number))
        {
            title_hidden = title_hidden.changeLetter(i, String.fromCharCode(number))
            correct = true;
        }
    }

    var elem = "letter" + number;

    if(correct==true)
    {
        document.getElementById(elem).style.background = "#007500";
        document.getElementById(elem).style.border = "2px solid #00C000";
        document.getElementById(elem).style.cursor = "default";
        document.getElementById(elem).style.color = "white";
        refresh_title();
    }
    else
    {
        document.getElementById(elem).style.background = "#750000";
        document.getElementById(elem).style.border = "2px solid #C00000";
        document.getElementById(elem).style.cursor = "default";
        document.getElementById(elem).style.color = "white";
        document.getElementById(elem).setAttribute("onclick", ";");
        missed++;
        var img = "/static/films/images/img/s"+missed+".jpg"
        document.getElementById("hangman").innerHTML = '<img class="hangman_img" src="'+img+'" alt="" />'
    }
    var height = document.getElementById("hangman_container").offsetHeight;
    // var height = document.getElementById("alphabet").getBoundingClientRect().bottom;
    if (title == title_hidden)
    {
        document.getElementById("result_card").style.display = "flex";
        document.getElementById("result_info").style.display = "block";
        document.getElementById("again").style.display = "block";
        document.getElementById("result_info").innerHTML = "You won! Answer: "+title;
        document.getElementById("result_card").innerHTML = text;
        document.getElementById("again").innerHTML = '<span class="reset" onclick="location.reload()">AGAIN?</span>';
        var elems = document.getElementsByClassName("letter")
        for(i=0;i<elems.length;i++)
        {
            elems[i].setAttribute("onclick", ";");
            elems[i].style.cursor = "default";
        }
        $("html, body").animate({scrollTop: height+30}, 1000);

    }
    if (missed >= 9)
    {
        document.getElementById("result_card").style.display = "flex";
        document.getElementById("result_info").style.display = "block";
        document.getElementById("again").style.display = "block";
        document.getElementById("result_info").innerHTML = "You lost! Correct answer: "+title;
        document.getElementById("result_card").innerHTML = text;
        document.getElementById("again").innerHTML = '<span class="reset" onclick="location.reload()">AGAIN?</span>';
        var elems = document.getElementsByClassName("letter");
        for(i=0;i<elems.length;i++)
        {
            elems[i].setAttribute("onclick", ";");
            elems[i].style.cursor = "default";
        }
        $("html, body").animate({scrollTop: height+30}, 1000);
    }
}

window.onload = start;