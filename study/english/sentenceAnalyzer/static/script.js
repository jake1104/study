document.getElementById('analyzeButton').addEventListener('click', async () => {
  const word = document.getElementById('wordInput').value;
  const response = await fetch(`/analyze?word=${word}`);
  const data = await response.json();
  
  document.getElementById('result').innerText = JSON.stringify(data, null, 2);
});
