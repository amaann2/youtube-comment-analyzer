import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getAnalysisData } from "../apis/youtube_analysis";
import toast from "react-hot-toast";
import DetailsBanner from "../components/Dashboard/DetailsBanner";
import SentimentChart from "../components/Dashboard/SentimentChart";
import Loader from "../components/Loader/Loader";
import WordCloud from "../components/Dashboard/WordCloud";
import TopComments from "../components/Dashboard/TopComments";
const Analysis = () => {
    const { id } = useParams();
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState(null);

    useEffect(() => {
        document.title = `Analysis - ${id}`; // Set the page title to the id
    }, [id]);
    useEffect(() => {
        const fetchData = async () => {
            try {
                const data = await getAnalysisData(id);
                setData(data);
                setLoading(false);
            } catch (error) {
                toast.error("Failed to load analysis data.");
            }
        };
        fetchData();
    }, [id]);
    if (!data && loading) {
        return <Loader />
    }
    const { video_details, sentiment_distribution, common_words, top_comments } = data;

    return (
        <div className="bg-gray-200 min-h-screen p-4">
            <DetailsBanner details={video_details} />
            <div className="flex flex-col lg:flex-row gap-4">
                <SentimentChart data={sentiment_distribution} />
                <WordCloud data={common_words} />
            </div>
            <TopComments comments={top_comments} video_details={video_details} />
        </div>
    );
};

export default Analysis;
