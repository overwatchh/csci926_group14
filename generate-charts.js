const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const chartFiles = fs.readdirSync('./charts')
  .filter(file => file.endsWith('.py'))
  .map(file => path.join('charts', file));

chartFiles.forEach(file => {
  exec(`python "${file}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error running ${file}:\n`, stderr);
    } else {
      console.log(`Output from ${file}:\n`, stdout);
    }
  });
});
