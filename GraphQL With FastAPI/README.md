## In this directory we are going learn fastapi with GraphQL.
    
### What is graphql?
GraphQL is a query language for APIs and a runtime for executing those queries by using a type system you define for your data. It allows clients to request exactly the data they need, making it more efficient and flexible than traditional REST APIs.

### Why GraphQL?
- Flexibility: Clients can request only the data they need, reducing over-fetching and under-fetching of data.
- Efficiency: Multiple resources can be fetched in a single request, reducing the number of network calls.
- Strongly Typed Schema: GraphQL APIs are defined by a schema that specifies the types of data and the relationships between them, providing clear documentation and validation.
- Real-time Data: GraphQL supports subscriptions, allowing clients to receive real-time updates when data changes.
- Developer Experience: GraphQL provides powerful tools for developers, including introspection and auto-generated documentation, making it easier to work with APIs.



### Let start with comparation between REST and GraphQL.

### Rest API: 
- Defination: REST (Representational State Transfer) is an architectural style for designing networked applications. It relies on stateless, client-server communication, typically over HTTP.
- In REST, resources are identified by URLs, and standard HTTP methods (GET, POST, PUT, DELETE) are used to perform operations on these resources.
- Each endpoint corresponds to a specific resource or collection of resources.


### GraphQL:
- Defination: GraphQL is a query language for APIs and a runtime for executing those queries by using a type system you define for your data. It allows clients to request exactly the data they need, making it more efficient and flexible than traditional REST APIs.
- In GraphQL, clients can specify the structure of the response, and multiple resources can be fetched in a single request.
- A single endpoint is used for all interactions, and the client defines the shape of the response.


### In GraphQL we have mainly two operations:
#### Query: 
* Used to read or fetch data from the server. It allows clients to specify exactly what data they need. 
* Query are similar to GET operations in REST.

#### Mutation: 
* Used to modify data on the server (create, update, delete). 
* In simple terms, mutations are like POST, PUT, DELETE operations in REST.


### FAQ:
1. Question: Can we perform query and mutation in a single request?

    > No, in GraphQL, queries and mutations are separate operations. A single request can either be a query or a mutation, but not both simultaneously. This separation helps maintain clarity and ensures that the operations are handled appropriately by the server.

2. Question: How does GraphQL handle versioning compared to REST?
    > In REST, versioning is often managed through URL paths (e.g., /api/v1/resource) or headers, which can lead to multiple versions of the API being maintained simultaneously. In contrast, GraphQL typically avoids versioning by allowing clients to request only the fields they need. This flexibility means that as the schema evolves, clients can continue to function without breaking changes, reducing the need for multiple versions of the API.

3. Question: What are some common use cases where GraphQL is preferred over REST?
    > GraphQL is often preferred in scenarios where clients require flexibility in data retrieval, such as mobile applications with varying data needs, complex applications that need to aggregate data from multiple sources, and situations where minimizing the number of network requests is crucial for performance.

4. Question: How does GraphQL handle errors compared to REST?
    > In REST, errors are typically communicated through HTTP status codes (e.g., 404 for Not Found, 500 for Server Error). In GraphQL, errors are returned in the response body alongside the data, allowing clients to receive partial data along with error information. This approach provides more context about what went wrong while still delivering any available data.

5. Question: So are you saying in Graphsql does not have status codes?

    > GraphQL primarily uses a single endpoint for all requests, and the HTTP status code is usually 200 OK for successful requests, regardless of whether the operation was a query or mutation. However, if there are errors in processing the request (e.g., syntax errors, validation errors), the server may return appropriate HTTP status codes like 400 Bad Request or 500 Internal Server Error. The actual error details are included in the response body, allowing clients to understand what went wrong while still receiving any valid data.  


In GraphQL There are challenges as well:

- Version management: As we seen in It there is always of existing this but when it is rest it is easy to manage versioning but in GraphQL it is bit difficult because we have single endpoint so instead of to create a new version we have to deprecate the fields.

- Performance issues: GraphQL queries can be complex and may lead to performance issues if not optimized properly. Over-fetching or under-fetching of data can occur if the queries are not designed efficiently.

- File uploading: GraphQL does not have built-in support for file uploads, which can be a challenge when dealing with media files.

- Caching: Caching can be more complex in GraphQL due to the dynamic nature of queries. Traditional caching mechanisms may not work effectively, requiring more sophisticated caching strategies.






### GraphQL Used by companies like:
- Facebook
- GitHub
- Shopify
- Twitter
- Pinterest

