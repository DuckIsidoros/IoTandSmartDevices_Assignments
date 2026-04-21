module.exports = async function (context, req) {
    context.res = {
        status: 200,
        body: { key: process.env.AZURE_MAPS_KEY },
        headers: { 'Content-Type': 'application/json' }
    };
};