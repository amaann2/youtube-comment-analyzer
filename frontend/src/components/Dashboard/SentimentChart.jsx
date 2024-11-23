import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

const SentimentChart = ({ data }) => {
    const total = data.Neutral + data.Positive + data.Negative;
    const getPercentage = (value) => ((value / total) * 100).toFixed(1);

    const sentimentChartData = [
        { name: "Neutral", value: data.Neutral, percentage: getPercentage(data.Neutral), color: "#64748b" },
        { name: "Positive", value: data.Positive, percentage: getPercentage(data.Positive), color: "#22c55e" },
        { name: "Negative", value: data.Negative, percentage: getPercentage(data.Negative), color: "#ef4444" }
    ];

    return (
        <div className="bg-white rounded-2xl shadow-lg py-6 px-8 w-full md:w-2/3 lg:w-1/2  border border-gray-100 ">
            <h2 className="text-2xl font-bold mb-6 text-[#0f0f0f] flex items-center">
                <svg viewBox="0 0 24 24" className="w-6 h-6 mr-3 fill-current text-red-600">
                    <path d="M16.5 3c-1.74 0-3.41.81-4.5 2.09C10.91 3.81 9.24 3 7.5 3 4.42 3 2 5.42 2 8.5c0 3.78 3.4 6.86 8.55 11.54L12 21.35l1.45-1.32C18.6 15.36 22 12.28 22 8.5 22 5.42 19.58 3 16.5 3zm-4.4 15.55l-.1.1-.1-.1C7.14 14.24 4 11.39 4 8.5 4 6.5 5.5 5 7.5 5c1.54 0 3.04.99 3.57 2.36h1.87C13.46 5.99 14.96 5 16.5 5c2 0 3.5 1.5 3.5 3.5 0 2.89-3.14 5.74-7.9 10.05z" />
                </svg>
                Audience Sentiment Analysis
            </h2>
            <div className="bg-gray-50 rounded-xl p-6 ">
                <ResponsiveContainer width="100%" height={400}>
                    <PieChart>
                        <Pie
                            data={sentimentChartData}
                            dataKey="value"
                            nameKey="name"
                            cx="50%"
                            cy="50%"
                            outerRadius="85%"
                            innerRadius="60%"
                            label={(entry) => `${entry.name} (${entry.percentage}%)`}
                            labelLine={false}
                        >
                            {sentimentChartData.map((entry, index) => (
                                <Cell
                                    key={`cell-${index}`}
                                    fill={entry.color}
                                    stroke="none"
                                />
                            ))}
                        </Pie>
                        <Tooltip
                            contentStyle={{
                                backgroundColor: '#fff',
                                border: 'none',
                                borderRadius: '8px',
                                boxShadow: '0 2px 8px rgba(0,0,0,0.15)'
                            }}
                            formatter={(value, name) => [`${getPercentage(value)}%`, name]}
                        />
                        <Legend
                            verticalAlign="bottom"
                            align="center"
                            iconType="circle"
                            wrapperStyle={{
                                paddingTop: '20px'
                            }}
                        />
                    </PieChart>
                </ResponsiveContainer>
            </div>
        </div>
    )
}

export default SentimentChart