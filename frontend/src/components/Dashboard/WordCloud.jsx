import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import cloud from 'd3-cloud';

const WordCloud = ({ data }) => {
    const svgRef = useRef(null);
    const containerRef = useRef(null);
    const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

    // Handle resize
    useEffect(() => {
        const updateDimensions = () => {
            if (containerRef.current) {
                const { width } = containerRef.current.getBoundingClientRect();
                setDimensions({
                    width: width,
                    height: Math.min(450, width * 0.7) // Maintain aspect ratio
                });
            }
        };

        window.addEventListener('resize', updateDimensions);
        updateDimensions();

        return () => window.removeEventListener('resize', updateDimensions);
    }, []);

    useEffect(() => {
        if (!data || !dimensions.width) return;

        // Clear previous content
        d3.select(svgRef.current).selectAll("*").remove();

        // Convert data to format needed by d3-cloud
        const maxValue = Math.max(...Object.values(data));
        const words = Object.entries(data).map(([text, value]) => ({
            text,
            size: 12 + (value / maxValue) * 130 // Scale font size between 12 and 60
        }));

        // Set up the layout
        const layout = cloud()
            .size([dimensions.width, dimensions.height])
            .words(words)
            .padding(5)
            .rotate(() => Math.random() > 0.5 ? 0 : 90) // Random rotation for visual interest
            .fontSize(d => d.size)
            .spiral('archimedean')
            .on("end", draw);

        // Start the layout
        layout.start();

        // Function to draw the word cloud
        function draw(words) {
            const colorScale = d3.scaleOrdinal()
                .range(['#2563eb', '#7c3aed', '#db2777', '#059669', '#ea580c']); // Custom color palette

            const svg = d3.select(svgRef.current)
                .attr("width", dimensions.width)
                .attr("height", dimensions.height)
                .append("g")
                .attr("transform", `translate(${dimensions.width / 2},${dimensions.height / 2})`);

            const texts = svg.selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", d => `${d.size}px`)
                .style("font-family", "'Inter', sans-serif")
                .style("font-weight", "600")
                .style("fill", d => colorScale(d.text))
                .attr("text-anchor", "middle")
                .attr("transform", d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
                .text(d => d.text)
                .style("opacity", 0);

            texts.transition()
                .duration(1000)
                .style("opacity", 1);

            texts.on("mouseenter", function () {
                d3.select(this)
                    .transition()
                    .duration(200)
                    .style("font-size", d => `${d.size * 1.2}px`)
                    .style("cursor", "pointer")
                    .style("filter", "brightness(120%)");
            })
                .on("mouseleave", function () {
                    d3.select(this)
                        .transition()
                        .duration(200)
                        .style("font-size", d => `${d.size}px`)
                        .style("filter", "brightness(100%)");
                });
        }
    }, [data, dimensions]);

    return (
        <div className="bg-white rounded-2xl shadow-lg py-6 px-8 w-full lg:w-1/2">
            <h2 className="text-2xl font-bold mb-6 text-[#0f0f0f] flex items-center">
                <svg viewBox="0 0 24 24" className="w-6 h-6 mr-3 fill-current text-blue-600">
                    <path d="M12.87 15.07l-2.54-2.51.03-.03c1.74-1.94 2.98-4.17 3.71-6.53H17V4h-7V2H8v2H1v1.99h11.17C11.5 7.92 10.44 9.75 9 11.35 8.07 10.32 7.3 9.19 6.69 8h-2c.73 1.63 1.73 3.17 2.98 4.56l-5.09 5.02L4 19l5-5 3.11 3.11.76-2.04zM18.5 10h-2L12 22h2l1.12-3h4.75L21 22h2l-4.5-12zm-2.62 7l1.62-4.33L19.12 17h-3.24z" />
                </svg>
                Most Used Words
            </h2>
            <div className="bg-gray-50 rounded-xl" ref={containerRef}>
                <div className="overflow-hidden flex justify-center">
                    <svg ref={svgRef} className="w-full" />
                </div>
            </div>
        </div>
    );
};

export default WordCloud;