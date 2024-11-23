import { useState } from "react";
import axios from "axios";
import toast from "react-hot-toast";
import { API_BASE_URL } from "../../config";
const TopComments = ({ comments, video_details }) => {
    const [expandedComments, setExpandedComments] = useState({});
    const [aiReplies, setAiReplies] = useState({});
    const [loadingIndex, setLoadingIndex] = useState(null);
    const generateAIReply = async (comment, index) => {
        console.log(comment)
        setLoadingIndex(index);
        try {
            const response = await axios.post(`${API_BASE_URL}/api/analysis/ai-reply`, {
                comment: comment,
                video_details
            });
            setAiReplies(prev => ({
                ...prev,
                [index]: response.data.reply
            }));
        } catch (error) {
            toast.error('Error generating AI reply');
        } finally {
            setLoadingIndex(null);
        }
    };

    const toggleReplies = (index) => {
        setExpandedComments(prev => ({
            ...prev,
            [index]: !prev[index]
        }));
    };

    return (
        <div className="bg-white rounded-2xl shadow-lg py-6 px-8 mt-4">
            <h2 className="text-2xl font-bold mb-6 text-[#0f0f0f] flex items-center">
                <svg viewBox="0 0 24 24" className="w-6 h-6 mr-3 fill-current text-purple-600">
                    <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z" />
                </svg>
                Most Engaging Comments & AI Responses
            </h2>
            <div className="space-y-6 h-[600px] overflow-y-auto pr-4">
                {comments?.map((comment, index) => (
                    <div
                        key={index}
                        className={`bg-gray-50 rounded-xl p-6 transition-all duration-300 ${loadingIndex === index
                            ? 'border-2 border-purple-500  relative'
                            : ''
                            }`}
                    >
                        {loadingIndex === index && (
                            <div className="absolute inset-0 bg-purple-50/50 rounded-xl flex items-center justify-center">
                                <div className="w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full animate-spin"></div>
                            </div>
                        )}
                        <div className="flex items-start justify-between">
                            <div className="flex items-start space-x-3">
                                <div className="flex-shrink-0">
                                    <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                                        <span className="text-white font-semibold">
                                            {comment.author[1]?.toUpperCase() || 'U'}
                                        </span>
                                    </div>
                                </div>
                                <div>
                                    <p className="font-semibold text-gray-900">{comment.author}</p>
                                    <p className="mt-1 text-gray-800">{comment.comment}</p>
                                    <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                                        <span className="flex items-center">
                                            <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 24 24">
                                                <path d="M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z" />
                                            </svg>
                                            {comment.like_count}
                                        </span>
                                        <span>{new Date(comment.published_at).toLocaleDateString()}</span>
                                        <button
                                            onClick={() => generateAIReply(comment, index)}
                                            className="inline-flex items-center text-purple-600 hover:text-purple-800"
                                            disabled={loadingIndex === index}
                                        >
                                            {loadingIndex === index ? (
                                                <span>AI...</span>
                                            ) : (
                                                <>
                                                    <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                                    </svg>
                                                    <span>Generate Reply from AI</span>
                                                </>
                                            )}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {aiReplies[index] && (
                            <div className="mt-4 ml-12 bg-purple-50 rounded-lg p-4 border border-purple-200">
                                <p className="text-gray-800 font-semibold">AI Reply:</p>
                                <p className="text-purple-800">{aiReplies[index]}</p>
                            </div>
                        )}

                        {comment.replies && comment.replies.length > 0 && (
                            <div className="mt-4">
                                <button
                                    onClick={() => toggleReplies(index)}
                                    className="ml-12 text-purple-600 hover:text-purple-800 font-medium"
                                >
                                    {expandedComments[index] ? 'Hide Replies' : `View ${comment.replies.length} Replies`}
                                </button>

                                {expandedComments[index] && (
                                    <div className="mt-4 ml-12 space-y-4">
                                        {comment.replies.map((reply, replyIndex) => (
                                            <div key={replyIndex} className="bg-white rounded-lg p-4 border border-gray-200">
                                                <div className="flex items-start space-x-3">
                                                    <div className="flex-shrink-0">
                                                        <div className="w-8 h-8 bg-gray-400 rounded-full flex items-center justify-center">
                                                            <span className="text-white text-sm font-semibold">
                                                                {reply.author[1]?.toUpperCase() || 'U'}
                                                            </span>
                                                        </div>
                                                    </div>
                                                    <div>
                                                        <p className="font-semibold text-gray-900">{reply.author}</p>
                                                        <p className="mt-1 text-gray-700">{reply.comment}</p>
                                                        <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                                                            <span className="flex items-center">
                                                                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 24 24">
                                                                    <path d="M1 21h4V9H1v12zm22-11c0-1.1-.9-2-2-2h-6.31l.95-4.57.03-.32c0-.41-.17-.79-.44-1.06L14.17 1 7.59 7.59C7.22 7.95 7 8.45 7 9v10c0 1.1.9 2 2 2h9c.83 0 1.54-.5 1.84-1.22l3.02-7.05c.09-.23.14-.47.14-.73v-2z" />
                                                                </svg>
                                                                {reply.like_count}
                                                            </span>
                                                            <span>{new Date(reply.published_at).toLocaleDateString()}</span>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default TopComments;