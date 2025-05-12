import React, { useState } from 'react';
import ReactDOM from 'react-dom';

const MyComponent = () => {
  const [text, setText] = useState('');
  const [answer, setAnswer] = useState('');

  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  const getAnswer = async () => {
    try {
      const response = await fetch('/get-answer', { params: { text } });
      setAnswer(response.data.answer);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <input type="text" value={text} onChange={handleTextChange} />
      <button onClick={getAnswer}>Get Answer</button>
      <p>{answer}</p>
    </div>
  );
};

ReactDOM.render(<MyComponent />, document.getElementById('root'));