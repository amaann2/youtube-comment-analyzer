import { Statistic } from "antd";
import { FaExternalLinkAlt, FaEye, FaThumbsUp, FaComments, FaYoutube, FaVideo } from "react-icons/fa";

const DetailsBanner = ({ details }) => {
    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
    return (
        <div className="bg-gradient-to-r from-white to-gray-50 rounded-3xl shadow-lg py-2 px-8 mb-8 mt-2 border border-gray-100">
            <div className="flex justify-between items-start mb-2">
                <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-blue-500 flex items-center gap-3">
                    <FaVideo className="text-purple-600" />
                    {details.title}
                </h1>
                <a
                    href={details.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:text-blue-700 transition-colors p-2 hover:bg-blue-50 rounded-full"
                >
                    <FaExternalLinkAlt size={24} />
                </a>
            </div>
            <p className="text-gray-600 text-sm mb-6 font-medium flex items-center gap-2">

                Published on {formatDate(details.published_at)}
            </p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <div className="bg-green-50 p-4 rounded-xl shadow-sm">
                    <Statistic
                        title={<span className="flex items-center gap-2"><FaEye className="text-green-600" /> Views</span>}
                        value={details.view_count}
                        valueStyle={{ color: "#3f8600", fontSize: '1.5rem' }}
                    />
                </div>
                <div className="bg-blue-50 p-4 rounded-xl shadow-sm">
                    <Statistic
                        title={<span className="flex items-center gap-2"><FaThumbsUp className="text-blue-600" /> Likes</span>}
                        value={details.like_count}
                        valueStyle={{ color: "#1890ff", fontSize: '1.5rem' }}
                    />
                </div>
                <div className="bg-orange-50 p-4 rounded-xl shadow-sm">
                    <Statistic
                        title={<span className="flex items-center gap-2"><FaComments className="text-orange-600" /> Comments</span>}
                        value={details.comment_count}
                        valueStyle={{ color: "#ff5722", fontSize: '1.5rem' }}
                    />
                </div>
                <div className="bg-purple-50 p-4 rounded-xl shadow-sm">
                    <Statistic
                        title={<span className="flex items-center gap-2"><FaYoutube className="text-purple-600" /> Channel</span>}
                        value={details.channel_title}
                        valueStyle={{ color: "#722ed1", fontSize: '1.5rem' }}
                    />
                </div>
            </div>
        </div>
    )
}

export default DetailsBanner