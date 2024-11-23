import "./loading.css";
const Loader = () => {
    return (
        <div className="loading-content flex flex-col items-center justify-center h-screen">
            <div className="loading">
                <div className="circle"></div>
                <div className="circle"></div>
                <div className="circle"></div>
            </div>
            <div className="mt-12 text-3xl ">Processing your analysis ...</div>
        </div>
    )
}

export default Loader