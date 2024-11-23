import { useState } from "react";
import { Button, Input } from "@relume_io/relume-ui";
import { analyzeComments } from "../../apis/youtube_analysis";
import toast from "react-hot-toast";
import Loader from "../Loader/Loader";
const Hero = () => {
    const [searchInput, setSearchInput] = useState("");
    const [maxComments, setMaxComments] = useState("6000");
    const [loading, setLoading] = useState(false);

    const validateForm = () => {
        if (!searchInput) {
            toast.error("Please enter a YouTube URL");
            return false;
        }

        try {
            new URL(searchInput);
            if (!searchInput.includes("youtube.com") && !searchInput.includes("youtu.be")) {
                toast.error("Please enter a valid YouTube URL");
                return false;
            }
        } catch (error) {
            toast.error("Please enter a valid URL");
            return false;
        }

        const maxCommentsNum = parseInt(maxComments);
        if (isNaN(maxCommentsNum) || maxCommentsNum <= 0) {
            toast.error("Please enter a valid number of comments");
            return false;
        }

        return true;
    };

    const navigateToAnalysisPage = (id) => {
        const modifiedUrl = `${window.location.origin}/analysis/${id}`;
        window.open(modifiedUrl, "_blank");

        // const link = document.createElement("a");
        // link.href = modifiedUrl;
        // link.target = "_blank";
        // link.style.display = "none";
        // document.body.appendChild(link);
        // link.click();
        // document.body.removeChild(link)
    }

    const handleSubmit = async (event) => {
        event.preventDefault();

        if (!validateForm()) return;

        try {
            setLoading(true);
            const response = await analyzeComments({ url: searchInput, max_comments: maxComments });
            setSearchInput("");
            navigateToAnalysisPage(response.id);
        } catch (error) {
            toast.error(error.message);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <Loader />
    }
    return (
        <section id="hero" className="relative h-screen w-full">
            <div className="absolute inset-0">
                <img
                    src="https://images.pexels.com/photos/95916/pexels-photo-95916.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
                    alt="A background showing analytics charts"
                    className="h-full w-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-b from-black via-black/60 to-transparent" />
            </div>

            <div className="relative z-10 flex h-full flex-col items-center pt-20 text-center text-white px-6">
                <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight leading-tight mb-6 animate-fadeIn">
                    Analyze Your YouTube Comments
                </h1>
                <p className="text-lg md:text-2xl font-light max-w-3xl mb-8 animate-slideUp delay-100 max-w-xxl">
                    Understand audience sentiment, detect spam, and get actionable insights for your videos. Paste a YouTube URL below to start analyzing.
                </p>
                <form
                    onSubmit={handleSubmit}
                    className="mt-6 flex w-full max-w-md flex-col md:flex-row items-center gap-4 animate-fadeInDelay"
                >
                    <div className="w-full flex flex-col gap-4">
                        <Input
                            id="search"
                            type="url"
                            placeholder="Enter YouTube video URL"
                            value={searchInput}
                            onChange={(e) => setSearchInput(e.target.value)}
                            className="w-full text-black bg-white rounded-lg shadow-md p-4 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                        />
                        <Input
                            id="maxComments"
                            type="text"
                            placeholder="6000"
                            value={maxComments}
                            onChange={(e) => setMaxComments(e.target.value)}
                            className="w-full text-black bg-white rounded-lg shadow-md p-4 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                        />
                        <Button
                            variant="primary"
                            size="lg"
                            className="bg-gradient-to-r from-blue-600 to-blue-400 text-white font-semibold rounded-lg px-6 py-4 shadow-lg hover:shadow-xl hover:from-blue-700 hover:to-blue-500 transition-all"
                            type="submit"
                        >
                            Analyze Now
                        </Button>
                    </div>
                </form>
            </div>
        </section>
    );
};

export default Hero;
