document.addEventListener('DOMContentLoaded', function() {
  // Function to change the background color of the "todo-btn" element
  function cngclr() {
    var btn = document.getElementById("todo-btn");
    btn.style.backgroundColor = '#8EACCD';
  }

  var btn = document.getElementById("todo-btn");

  // Add event listeners for mousedown and mouseup events on the "todo-btn" element
  btn.addEventListener("mousedown", cngclr);
  btn.addEventListener("mouseup", function() {
    btn.style.backgroundColor = '#cae1e5a3';
  });

  // Get all elements with the class "timer-btn"
  const buttons = document.querySelectorAll(".timer-btn");

  // Loop through each button and add event listeners
  buttons.forEach(function(button) {
    // Add mousedown event listener to change the background color
    button.addEventListener("mousedown", function() {
      button.style.backgroundColor = '#8EACCD';
    });
  
    // Add mouseup event listener to reset the background color
    button.addEventListener("mouseup", function() {
      button.style.backgroundColor = '#cae1e5a3';
    });
  
    // Add click event listener to handle start/stop timer functionality
    button.addEventListener("click", function(e) {
      // Get the text content of the button
      text = button.innerText;
  
      // If the button text is "Start timer", start the timer
      if (text == "Start timer") {
        if (startTimer(e)) {
          button.innerText = "Stop";
          buttons.forEach(function(otherButton) {
            if (otherButton != e.target) {
              otherButton.disabled = true; // Disable all other buttons
            }
          });
        }
      }
      // If the button text is "Stop", stop the timer
      else if (text == "Stop") {
        button.innerText = "Start timer";
        stopTimer(e);
        buttons.forEach(function(otherButton) {
          otherButton.disabled = false; // Enable all buttons
        });
      }
    });
  });
  // Function to add a new todo item
  function add_todo() {
    // Get the value from the todo input field
    const todo_text = document.getElementById('todo-input').value;

    // If the input is empty, return
    if (todo_text == '') {
      return 0;
    }

    // Create a new list item element for the todo
    const todo = document.createElement('li');
    todo.innerText = todo_text;
    todo.classList.add('list-itm', 'td-itm');

    // Get the todo list container and append the new todo item
    const todo_cont = document.getElementById('list-container');
    todo_cont.appendChild(todo);

    // Add a close button (cross) to the todo item
    let span = document.createElement("span");
    span.innerHTML = "\u00d7";
    todo.appendChild(span);

    // Send the new todo item to the server
    fetch('/addtodo', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({ task: todo_text }),
    });
  }

  // Function to toggle the status (checked/unchecked) of a todo item and delete a todo item
  function change_status() {
    // Get the todo list container
    listContainer = document.getElementById('list-container');

    // Add a click event listener to the todo list container
    listContainer.addEventListener("click", function(e) {
      // If the clicked element is a list item, toggle the "checked" class
      if (e.target.tagName === "LI") {
        e.target.classList.toggle("checked");
      }
      // If the clicked element is a span (close button), remove the todo item and delete it from the server
      else if (e.target.tagName === "SPAN") {
        e.target.parentElement.remove();
        text = e.target.parentElement.innerText;
        text = text.replace('\u00d7', '');
        text = text.trim();
        delete_todo(text);
      }
    });
  }

  // Function to delete a todo item from the server
  function delete_todo(text) {
    fetch('/deletetodo', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({ task: text }),
    });
  }

  // Add event listeners for the "todo-btn" and the todo list container
  btn.addEventListener("click", add_todo);
  listContainer = document.getElementById('list-container');
  listContainer.addEventListener("click", change_status);
});

var running = false;
var animationFrameId;

// Function to update the stopwatch timer
function startStopwatch(e, tracked, startTime) {
  function updateTime(e) {
    elapsedTime = Date.now() - startTime + tracked;
    let hours = Math.floor(elapsedTime / (1000 * 60 * 60));
    let minutes = Math.floor((elapsedTime % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((elapsedTime % (1000 * 60)) / 1000);

    // Update the timer display
    var div = e.target.closest('.tra-container');
    var clk = div.querySelector('#clock');
    clk.innerText = hours + ":" + minutes + ":" + seconds;

    // Request the next animation frame to update the timer
    animationFrameId = requestAnimationFrame(() => updateTime(e));
    return elapsedTime;
  }

  updateTime(e);
}

// Function to start the timer
async function startTimer(e) {
  // Get the timer display element and extract the task text
  var div = e.target.closest('.tra-container');
  var text = div.querySelector('.tra-itm');
  text1 = text.innerText;
  text1 = text1.split("\n")[0];

  // Get the tracked time for the task from the server
  tracked = await get_trackedtime(text1);
  console.log(tracked);

  // If the timer is already running, don't start a new one
  if (running == true) {
    alert("timer already running");
    return false;
  } else {
    startTime = Date.now();
    running = true;
    animationFrameId = requestAnimationFrame(() => startStopwatch(e, tracked, startTime));
    return true;
  }
}

// Function to stop the timer
async function stopTimer(e) {
  running = false;
  var elapsed_time = Date.now() - startTime;
  let hours = Math.floor(elapsedTime / (1000 * 60 * 60));
  let minutes = Math.floor((elapsedTime % (1000 * 60 * 60)) / (1000 * 60));
  let seconds = Math.floor((elapsedTime % (1000 * 60)) / 1000);
  console.log(startTime, elapsed_time);
  console.log(hours + ":" + minutes + ":" + seconds);

  // Cancel the animation frame and update the tracked time on the server
  cancelAnimationFrame(animationFrameId);
  var div = e.target.closest('.tra-container');
  var text = div.querySelector('.tra-itm');
  text1 = text.innerText;
  text1 = text1.split("\n")[0];

  const response = await fetch('/updatetime', {
    method: 'POST',
    headers: {
      'Content-type': 'application/json',
    },
    body: JSON.stringify({ time: elapsed_time, text: text1 })
  });
}

// Function to get the tracked time for a task from the server
async function get_trackedtime(text1) {
  try {
    const response = await fetch('/gettime', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({ text: text1 }),
    });

    if (response.ok) {
      const data = await response.json();
      return data.message;
    } else {
      console.error('Error getting tracked time:', response.status);
      return 0;
    }
  } catch (error) {
    console.error('Error getting tracked time:', error);
    return 0;
  }
}
//https://stackoverflow.com/questions/6396101/pure-javascript-send-post-data-without-a-form 