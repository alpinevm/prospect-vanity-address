const robot = require('robotjs');

// Simulate CONTROL+OPTION+M keypress
robot.keyToggle('m', 'down', ['control', 'alt']);
robot.keyToggle('m', 'up', ['control', 'alt']);

// Simulate CONTROL+OPTION+N keypress
robot.keyToggle('n', 'down', ['control', 'alt']);
robot.keyToggle('n', 'up', ['control', 'alt']);

console.log('Keypress task executed successfully.');
