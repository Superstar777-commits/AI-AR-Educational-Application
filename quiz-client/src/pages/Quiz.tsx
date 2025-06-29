import { useParams } from "react-router";
import { useEffect, useRef, useState } from 'react';
import { Check } from "lucide-react";

interface Question{
    id: number;
    question: string;
    marks: number;
    level: "low" | "medium" | "high";
    correctAnswer: string;
    done: boolean;
    quiz_id: number;
    startTime?: string;
    endTime?: string;
}

interface Entry<K, V>{
    key: K;
    value: V;
}

function Quiz() {
    const {id, title, duration} = useParams();
    const [questions, setQuestions] = useState<Question[]>([]);
    const [error, setError] = useState<any>();
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const targetTimeRef = useRef(0);
    const [timeRemaining, setTimeRemaining] = useState<number>(Number(duration)*60000);
    const [countdownStarted, setCountdownStarted] = useState<boolean>(false);
    const [info, setInfo] = useState<any>();
    const [stack, setStack] = useState<Entry<string, number>[]>([]);

    useEffect(() => {
        const fetchData = async() => {
            setIsLoading(true);
            const response = await fetch(`http://127.0.0.1:8000/questions/quiz/${id}`);

            if(!response.ok){
                setError(response.statusText);
                setIsLoading(false);
                return;
            }

            const data: Question[] = await response.json();

            if(data.length === 0){
                setInfo("No questions in this quiz");
                setIsLoading(false);
                return;
            }

            setQuestions(data);
            setIsLoading(false);
            return;
        }

        fetchData();
    }, []);

    useEffect(() => {
        let intervalId: any;
        if (countdownStarted && targetTimeRef.current > 0) {
            intervalId = setInterval(() => {
                const currentTime = new Date().getTime();
                let calculatedRemainingTime = targetTimeRef.current - currentTime;

                if (calculatedRemainingTime <= 0) {
                    calculatedRemainingTime = 0;
                    alert("Time is up!")
                    setCountdownStarted(false);
                    clearInterval(intervalId);
                    targetTimeRef.current = 0;
                }
                setTimeRemaining(calculatedRemainingTime);
            }, 1000);
            return () => clearInterval(intervalId);
        } else if (!countdownStarted && intervalId) {
            clearInterval(intervalId);
        }
    }, [countdownStarted]);

    useEffect(() => {
        const newDurationMs = Number(duration)*60000;
        setTimeRemaining(newDurationMs);
        if (!countdownStarted) {
            targetTimeRef.current = 0;
        }
    }, [duration]);

    const formatTime = (ms: number) => {
        const totalSeconds = Math.max(0, Math.floor(ms / 1000));
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;

        return [hours, minutes, seconds]
            .map(unit => String(unit).padStart(2, '0'))
            .join(':');
    };

    const handleStartQuiz = () => {
        setCountdownStarted(true);
        setQuestions((prev) => {
            return prev.map((q) => {
                return {...q, done: false}
            })
        })
        if (targetTimeRef.current === 0 || timeRemaining === Number(duration)*60000) {
            targetTimeRef.current = new Date().getTime() + Number(duration)*60000;
        } else {
            targetTimeRef.current = new Date().getTime() + timeRemaining;
        }
    }

    const handleDoneQuestion = (questionId: number) => {
        setQuestions((prev) => {
            // Use .map() to create a NEW array
            return prev.map((question) => {
                if(question.id === questionId){
                    // Return a NEW object with the 'done' property updated
                // Spread the existing 'question' properties first to keep them
                return { ...question, done: true, endTime: new Date().getTime().toString() };
                }
                // if it's not the question we're looking for, return it unchaged
                return question;
            })
        });
    }

    // const handleAddHesitation = (questionId: number) => {

    // }

    if(isLoading){
        return(
            <div role="status">
    <svg aria-hidden="true" className="w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
        <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
    </svg>
    <span className="sr-only">Loading...</span>
</div>
        )
    }

    if(info){
        return(
            <div>
                <div className="mb-10 flex flex-col gap-2 text-left">
        <h1>{title}</h1>
      <h2>Duration: {duration} Mins</h2>
      </div>
            <p className='bg-blue-600 p-2 rounded-md text-white'>{info}</p>
        </div>
        )
    }

    if(error){
        return(
            <div>
                <p className='bg-red-500 p-2 rounded-md text-white'>Error fetching questions: {error}</p>
            </div>
        )
    }

  return (
    <div>
      <div className="mb-10 flex flex-col gap-2 text-left">
        <h1>{title}</h1>
      <h2>Duration: {duration} Mins</h2>
      {countdownStarted ? (formatTime(timeRemaining)) : (<></>)}
      {countdownStarted ? (<></>):(<button className="bg-green-500 p-2 rounded-md" type="button" onClick={() => handleStartQuiz()}><p>Start</p></button>)}
      </div>

      {questions.map((question: Question) => (
        <div key={question.id} className="mb-5 flex flex-col items-center">
            <label htmlFor={String(question.id)}>{question.question}</label>
            <input type="text" id={String(question.id)} className="border border-white" autoComplete="off" onFocus={() => question.startTime = new Date().getTime().toString()} disabled={question.done}/>
            {countdownStarted ? (<>
                <button className={question.done ? 'bg-green-500' : ''} onClick={() => handleDoneQuestion(question.id)}>
                {question.done ? (<Check />) : (<p>Mark as complete</p>)}
            </button>
            <p>Start time: {question.startTime}</p>
            <p>End time: {question.endTime}</p>
            </>): (<></>)}
        </div>
      ))}

      </div>
  )
}

export default Quiz