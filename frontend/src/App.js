import './App.css';
import React, { useState, useRef } from 'react';


function _romanize (num) {
    if (isNaN(num))
        return NaN;
    var digits = String(+num).split(""),
        key = ["","C","CC","CCC","CD","D","DC","DCC","DCCC","CM",
               "","X","XX","XXX","XL","L","LX","LXX","LXXX","XC",
               "","I","II","III","IV","V","VI","VII","VIII","IX"],
        roman = "",
        i = 3;
    while (i--)
        roman = (key[+digits.pop() + (i * 10)] || "") + roman;
    return Array(+digits.join("") + 1).join("M") + roman;
}

function TopLevelCheckbox(props) {
  let lis = [];

  const t = e => {
    props.onChange(e, props.bookName)
  }

  // my approach of passing the parent props with {...props} is a bit risky because we pass onChange
  // to TopLevelCheckbox but that needs to be wrapped with the function t. just be aware of it...
  return (
    <li className="mt-1" ><input  checked={props.checked} type="checkbox" onChange={t}/> {props.bookName === 0 ? "Intro and POW" : props.prefix + props.bookName}
      <ul className="pl-5">
        {lis}
      </ul>
    </li>
    )
}

function App() {
  // const [answer, setAnswer] = useState("Adam Smith means that progressing states are those in which society is advancing to the further acquisition of wealth and riches. He states that the condition of the labouring poor is happiest and most comfortable in the progressive state, while it is hard in the stationary state and miserable in the declining state. He also states that wages of labour would have augmented with improvements in its productive powers in the progressive state.");
  // const [sources, setSources] = useState([{"text": "It deserves to be remarked, perhaps, that it is in the progressive state, while the society is advancing to the further acquisition, rather than when it has acquired its full complement of riches, that the condition of the labouring poor, of the great body of the people, seems to be the happiest and the most comfortable. It is hard in the stationary, and miserable in the declining state. The progressive state is, in reality, the cheerful and the hearty state to all the different orders of the society; the stationary is dull; the declining melancholy.", "info": "Chapter 1.0. Book 8.0. Paragraph 40."}, {"text": "Had this state continued, the wages of labour would have augmented with all those improvements in its productive powers, to which the division of labour gives occasion. All things would gradually have become cheaper. They would have been produced by a smaller quantity of labour; and as the commodities produced by equal quantities of labour would naturally in this state of things be exchanged for one another, they would have been purchased likewise with the produce of a smaller quantity.", "info": "Chapter 1.0. Book 8.0. Paragraph 1."}, {"text": "In some cases, the state of society necessarily places the greater part of individuals in such situations as naturally form in them, without any attention of government, almost all the abilities and virtues which that state requires, or perhaps can admit of. In other cases, the state of the society does not place the greater part of individuals in such situations; and some attention of government is necessary, in order to prevent the almost entire corruption and degeneracy of the great body of the people.", "info": "Chapter 5.0. Book 1.0. Paragraph 181."}]);
  // const [searchText, setSearchText] = useState("What does Adam Smith mean by the progressive state?"); // What does Adam Smith mean by the progressive state?
  
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [searchText, setSearchText] = useState("");
  const [bookNames, setBookNames] = useState({"wealth_of_nations": [0,1,2,3,4,5], "leviathan": [1,2,3,4]}) // 1,2,3,4,5
  const [selectedBook, setSelectedBook] = useState("leviathan")

  const inputRef = useRef(null);

  const handleChange = e => {
    setSearchText(e.target.value);
  };

  const renderSources = () => {
    if (sources.length !== 0) {
      const listItems = sources.map(
        (d) => (
          <div>
            <h1 className="text-lg">{d.info}</h1>
            <p><i>{d.text}</i></p>
            <br/>
          </div>
          ))
      return (
        <div>
          <h1 className="text-xl">Sources</h1>
          {listItems}
        </div>
        )
    }
  }

  const handleSubmit = e => {
    e.preventDefault()
    setAnswer("Loading...")
    setSources([])
    inputRef.current.blur()

    if (searchText.trim() === "") {
      setAnswer("Please enter a query into the search box.")
      return
    } else if (bookNames[selectedBook].length === 0) {
      setAnswer("Please select at least one book.")
      return
    }

    fetch("http://localhost:5000/?book=" + selectedBook + "&query=" + searchText + "&books=[" + bookNames[selectedBook] + "]")
      .then(res => {
        if (!res.ok) {
          setAnswer("Unfortunately, we have encountered an error. Please alert Khush with the following error message: error with request. " + res.statusText)
          throw Error(res.statusText)
        }
        return res;
      })
      .then(res => res.json())
      .then(
        (result) => {
          if (result.status === 0) {
            console.log(result.answer)
            setAnswer(result.answer)
            setSources(result.sources)
          } else {
            setAnswer("Unfortunately, we have encountered an error. Please alert Khush with the following error message: " + result.msg)
          }
          
        })
      .catch(err => {
        setAnswer("Unfortunately, we have encountered an internal error. Please alert Khush!")
        throw err;
      })
  };

  const appendBook = (e,n) => {
    console.log('n', n)
    let target_list = bookNames[selectedBook];
    if (e.target.checked) {
      target_list = target_list.concat([n])
    } else {
      let index = target_list.indexOf(n)
      target_list.splice(index, 1)
    }
    setBookNames({...bookNames, [selectedBook]: target_list})
  }
  console.log(bookNames)

  const generateSectionOptions = () => {
    let l = []
    if (selectedBook === "wealth_of_nations") {
      l.push(<TopLevelCheckbox onChange={appendBook} bookName={0} prefix={"Intro and POW"} checked={bookNames[selectedBook].includes(0)}/>)
      for (let i = 1; i <= 5; i++) {
        l.push(<TopLevelCheckbox onChange={appendBook} bookName={i} prefix={"Chapter "} checked={bookNames[selectedBook].includes(i)}/>)
      }
    } else if (selectedBook === "leviathan") {
      for (let i = 1; i <= 4; i++) {
        l.push(<TopLevelCheckbox onChange={appendBook} bookName={i} prefix={"Part "} checked={bookNames[selectedBook].includes(i)}/>)
      }
    }

    return (
      <ul className="list-none">
        {l}
        {/*<TopLevelCheckbox onChange={appendBook} bookName={0} />
        <TopLevelCheckbox onChange={appendBook} bookName={1} numChapters={11} hasIntro="yes"/>
        <TopLevelCheckbox onChange={appendBook} bookName={2} numChapters={5}/>
        <TopLevelCheckbox onChange={appendBook} bookName={3} numChapters={4}/>
        <TopLevelCheckbox onChange={appendBook} bookName={4} numChapters={9}/>
        <TopLevelCheckbox onChange={appendBook} bookName={5} numChapters={3}/>*/}
      </ul>
    )
  }

  return (
    <div className="flex my-10 font-serif">
      <div className="mx-10">
        <h1 className="text-xl">Options</h1>
        <h1 className="text-lg">Book</h1>
        <select onChange={(e) => {setSelectedBook(e.target.value)}} name="cars" id="cars">
          <option value="leviathan">Leviathan</option>
          <option value="wealth_of_nations">The Wealth of Nations</option>
        </select>
        {/*<h1 className="text-lg">No. Paragraphs</h1>
        <input
          // className="flex-grow px-2 !outline-none border-transparent focus:border-transparent focus:ring-0"
          type = "number" 
          placeholder = "Ask anything about the Wealth of Nations..." 
          onChange = {(e) => setNumClosest(e.target.value)}
          value={numClosest}
          // ref={inputRef}
          autoFocus
        />*/}
        <h1 className="text-lg mt-2">Content Included</h1>
        {generateSectionOptions()}
      </div>
      <div className="w-2/3">
        <form className="flex flex-row space-x-2 px-2 py-2 text-lg border border-black rounded-lg" onSubmit={handleSubmit}>
          <p>🔎</p>
          <input
            className="flex-grow px-2 !outline-none border-transparent focus:border-transparent focus:ring-0"
            type = "search" 
            placeholder = "Ask anything about the Leviathan..." 
            onChange = {handleChange}
            value={searchText}
            ref={inputRef}
            autoFocus
          />
        </form>
        
        
        {/*Bottom Half*/}
        <div className="">
          <div className="relative flex py-2 items-center">
            {/*<div className="flex-grow border-t border-gray-400"></div>*/}
          </div>
          <div className="px-2">
            <p className="">{answer}</p>
            <br/>
            {renderSources()}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
